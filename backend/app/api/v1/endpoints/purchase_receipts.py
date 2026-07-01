from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_superuser, get_current_user
from app.core.database import get_db
from app.integrations.inventory_auto_engine import StockEngine
from app.models.purchase_order import PurchaseOrder
from app.models.purchase_receipt import PurchaseReceipt
from app.models.purchase_receipt_item import PurchaseReceiptItem
from app.models.inventory_stock_movement import InventoryStockMovement
from app.models.user import User
from app.models.warehouse import Warehouse
from app.schemas.purchase_receipt import PurchaseReceiptCreate, PurchaseReceiptResponse

router = APIRouter()


def _next_receipt_number(db: Session) -> str:
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    count_today = (
        db.query(func.count(PurchaseReceipt.id))
        .filter(PurchaseReceipt.receipt_number.like(f"GR-{today}-%"))
        .scalar()
    )
    return f"GR-{today}-{count_today + 1:04d}"


@router.get("/", response_model=list[PurchaseReceiptResponse])
def list_receipts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    order_id: UUID | None = None,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    query = db.query(PurchaseReceipt).filter(PurchaseReceipt.is_deleted == False)
    if order_id:
        query = query.filter(PurchaseReceipt.order_id == order_id)
    return (
        query.order_by(PurchaseReceipt.receipt_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/{receipt_id}", response_model=PurchaseReceiptResponse)
def get_receipt(
    receipt_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    receipt = (
        db.query(PurchaseReceipt)
        .filter(PurchaseReceipt.id == receipt_id, PurchaseReceipt.is_deleted == False)
        .first()
    )
    if not receipt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Goods receipt not found")
    return receipt


@router.post("/", response_model=PurchaseReceiptResponse, status_code=status.HTTP_201_CREATED)
def create_receipt(
    receipt_in: PurchaseReceiptCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """Records goods received against a purchase order: updates each
    order line's received_quantity, posts an IN stock movement per item
    (which updates InventoryBalance via weighted-average cost), and marks
    the order RECEIVED once every line is fully received."""
    order = (
        db.query(PurchaseOrder)
        .filter(PurchaseOrder.id == receipt_in.order_id, PurchaseOrder.is_deleted == False)
        .first()
    )
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase order not found")
    if order.status not in ("APPROVED", "RECEIVED"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only approved purchase orders can receive goods",
        )

    warehouse = (
        db.query(Warehouse)
        .filter(Warehouse.id == receipt_in.warehouse_id, Warehouse.is_deleted == False)
        .first()
    )
    if not warehouse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Warehouse not found")

    order_items_by_product = {item.product_id: item for item in order.items}

    for receipt_item in receipt_in.items:
        order_item = order_items_by_product.get(receipt_item.product_id)
        if not order_item:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product {receipt_item.product_id} is not on this purchase order",
            )
        remaining = order_item.quantity - order_item.received_quantity
        if receipt_item.quantity > remaining:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Cannot receive {receipt_item.quantity} of product {receipt_item.product_id}: "
                    f"only {remaining} remaining on the order"
                ),
            )

    receipt_total = sum(item.quantity * item.unit_cost for item in receipt_in.items)

    receipt = PurchaseReceipt(
        receipt_number=_next_receipt_number(db),
        order_id=order.id,
        supplier_id=order.supplier_id,
        branch_id=order.branch_id,
        warehouse_id=receipt_in.warehouse_id,
        total=receipt_total,
        is_posted=True,
        created_by=current_user.id,
    )
    db.add(receipt)
    db.flush()

    stock_engine = StockEngine()

    for receipt_item in receipt_in.items:
        order_item = order_items_by_product[receipt_item.product_id]

        db.add(
            PurchaseReceiptItem(
                receipt_id=receipt.id,
                product_id=receipt_item.product_id,
                quantity=receipt_item.quantity,
                unit_cost=receipt_item.unit_cost,
                total=receipt_item.quantity * receipt_item.unit_cost,
                created_by=current_user.id,
            )
        )

        order_item.received_quantity += receipt_item.quantity

        movement = InventoryStockMovement(
            product_id=receipt_item.product_id,
            warehouse_id=receipt_in.warehouse_id,
            movement_type="IN",
            quantity=receipt_item.quantity,
            unit_cost=receipt_item.unit_cost,
            reference_type="PURCHASE",
            reference_id=receipt.id,
            created_by=current_user.id,
        )
        db.add(movement)
        db.flush()
        stock_engine.update_balance_from_movement(db, movement)

    db.flush()
    fully_received = all(item.received_quantity >= item.quantity for item in order.items)
    if fully_received:
        order.status = "RECEIVED"
        order.updated_by = current_user.id
        db.add(order)

    db.commit()
    db.refresh(receipt)
    return receipt
