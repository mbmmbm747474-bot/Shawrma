from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_superuser, get_current_user
from app.core.database import get_db
from app.models.branch import Branch
from app.models.product import Product
from app.models.purchase_order import PurchaseOrder
from app.models.purchase_order_item import PurchaseOrderItem
from app.models.supplier import Supplier
from app.models.user import User
from app.schemas.purchase_order import (
    PurchaseOrderCreate,
    PurchaseOrderResponse,
    PurchaseOrderUpdate,
)

router = APIRouter()


def _next_order_number(db: Session) -> str:
    """PO-YYYYMMDD-NNNN, sequential within the day. Not safe under heavy
    concurrent writes (a tiny race window between the count and the insert),
    but the order_number column is UNIQUE, so a collision fails loudly
    instead of silently corrupting data - acceptable for this stage."""
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    count_today = (
        db.query(func.count(PurchaseOrder.id))
        .filter(PurchaseOrder.order_number.like(f"PO-{today}-%"))
        .scalar()
    )
    return f"PO-{today}-{count_today + 1:04d}"


def _compute_totals(items_subtotal: float, discount: float, tax: float) -> float:
    return items_subtotal - discount + tax


@router.get("/", response_model=list[PurchaseOrderResponse])
def list_purchase_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    status_filter: str | None = None,
    supplier_id: UUID | None = None,
    branch_id: UUID | None = None,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    query = db.query(PurchaseOrder).filter(PurchaseOrder.is_deleted == False)
    if status_filter:
        query = query.filter(PurchaseOrder.status == status_filter)
    if supplier_id:
        query = query.filter(PurchaseOrder.supplier_id == supplier_id)
    if branch_id:
        query = query.filter(PurchaseOrder.branch_id == branch_id)
    return (
        query.order_by(PurchaseOrder.order_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/{order_id}", response_model=PurchaseOrderResponse)
def get_purchase_order(
    order_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    order = (
        db.query(PurchaseOrder)
        .filter(PurchaseOrder.id == order_id, PurchaseOrder.is_deleted == False)
        .first()
    )
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase order not found")
    return order


@router.post("/", response_model=PurchaseOrderResponse, status_code=status.HTTP_201_CREATED)
def create_purchase_order(
    order_in: PurchaseOrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    supplier = (
        db.query(Supplier)
        .filter(Supplier.id == order_in.supplier_id, Supplier.is_deleted == False)
        .first()
    )
    if not supplier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")

    branch = (
        db.query(Branch)
        .filter(Branch.id == order_in.branch_id, Branch.is_deleted == False)
        .first()
    )
    if not branch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Branch not found")

    product_ids = [item.product_id for item in order_in.items]
    found_products = (
        db.query(Product.id)
        .filter(Product.id.in_(product_ids), Product.is_deleted == False)
        .all()
    )
    found_ids = {p.id for p in found_products}
    missing = set(product_ids) - found_ids
    if missing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown product id(s): {', '.join(str(m) for m in missing)}",
        )

    subtotal = sum(item.quantity * item.unit_cost for item in order_in.items)
    total = _compute_totals(subtotal, order_in.discount, order_in.tax)

    order = PurchaseOrder(
        order_number=_next_order_number(db),
        supplier_id=order_in.supplier_id,
        branch_id=order_in.branch_id,
        status="DRAFT",
        subtotal=subtotal,
        discount=order_in.discount,
        tax=order_in.tax,
        total=total,
        created_by=current_user.id,
    )
    db.add(order)
    db.flush()

    for item in order_in.items:
        db.add(
            PurchaseOrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_cost=item.unit_cost,
                total=item.quantity * item.unit_cost,
                notes=item.notes,
                created_by=current_user.id,
            )
        )

    db.commit()
    db.refresh(order)
    return order


@router.put("/{order_id}", response_model=PurchaseOrderResponse)
def update_purchase_order(
    order_id: UUID,
    order_in: PurchaseOrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    order = (
        db.query(PurchaseOrder)
        .filter(PurchaseOrder.id == order_id, PurchaseOrder.is_deleted == False)
        .first()
    )
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase order not found")

    if order.status != "DRAFT":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only draft purchase orders can be edited",
        )

    update_data = order_in.model_dump(exclude_unset=True)
    new_items = update_data.pop("items", None)

    if "supplier_id" in update_data:
        supplier = (
            db.query(Supplier)
            .filter(Supplier.id == update_data["supplier_id"], Supplier.is_deleted == False)
            .first()
        )
        if not supplier:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")

    for field, value in update_data.items():
        setattr(order, field, value)

    if new_items is not None:
        product_ids = [item["product_id"] for item in new_items]
        found_products = (
            db.query(Product.id)
            .filter(Product.id.in_(product_ids), Product.is_deleted == False)
            .all()
        )
        found_ids = {p.id for p in found_products}
        missing = set(product_ids) - found_ids
        if missing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown product id(s): {', '.join(str(m) for m in missing)}",
            )

        # Replace all line items rather than diffing - simpler and correct
        # since this is only allowed while still in DRAFT.
        db.query(PurchaseOrderItem).filter(PurchaseOrderItem.order_id == order.id).delete()
        subtotal = 0.0
        for item in new_items:
            line_total = item["quantity"] * item["unit_cost"]
            subtotal += line_total
            db.add(
                PurchaseOrderItem(
                    order_id=order.id,
                    product_id=item["product_id"],
                    quantity=item["quantity"],
                    unit_cost=item["unit_cost"],
                    total=line_total,
                    notes=item.get("notes"),
                    created_by=current_user.id,
                )
            )
        order.subtotal = subtotal

    order.total = _compute_totals(order.subtotal, order.discount, order.tax)
    order.updated_by = current_user.id

    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.post("/{order_id}/approve", response_model=PurchaseOrderResponse)
def approve_purchase_order(
    order_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    order = (
        db.query(PurchaseOrder)
        .filter(PurchaseOrder.id == order_id, PurchaseOrder.is_deleted == False)
        .first()
    )
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase order not found")
    if order.status != "DRAFT":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only draft purchase orders can be approved",
        )
    if not order.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot approve a purchase order with no items",
        )

    order.status = "APPROVED"
    order.updated_by = current_user.id
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.post("/{order_id}/cancel", response_model=PurchaseOrderResponse)
def cancel_purchase_order(
    order_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    order = (
        db.query(PurchaseOrder)
        .filter(PurchaseOrder.id == order_id, PurchaseOrder.is_deleted == False)
        .first()
    )
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase order not found")
    if order.status == "RECEIVED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A fully received purchase order cannot be cancelled",
        )

    order.status = "CANCELLED"
    order.updated_by = current_user.id
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_purchase_order(
    order_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> None:
    order = (
        db.query(PurchaseOrder)
        .filter(PurchaseOrder.id == order_id, PurchaseOrder.is_deleted == False)
        .first()
    )
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase order not found")
    if order.status != "DRAFT":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only draft purchase orders can be deleted",
        )

    order.is_deleted = True
    order.deleted_at = datetime.now(timezone.utc)
    order.deleted_by = current_user.id
    db.add(order)
    db.commit()
    return None
