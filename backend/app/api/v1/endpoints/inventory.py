from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_superuser, get_current_user
from app.core.database import get_db
from app.integrations.inventory_auto_engine import StockEngine
from app.models.inventory_balance import InventoryBalance
from app.models.inventory_stock_movement import InventoryStockMovement
from app.models.product import Product
from app.models.user import User
from app.models.warehouse import Warehouse
from app.schemas.inventory import (
    InventoryBalanceResponse,
    StockAdjustmentCreate,
    StockMovementResponse,
)

router = APIRouter()


@router.get("/balances", response_model=list[InventoryBalanceResponse])
def list_balances(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    warehouse_id: UUID | None = None,
    product_id: UUID | None = None,
    skip: int = 0,
    limit: int = 200,
) -> Any:
    query = db.query(InventoryBalance)
    if warehouse_id:
        query = query.filter(InventoryBalance.warehouse_id == warehouse_id)
    if product_id:
        query = query.filter(InventoryBalance.product_id == product_id)
    return query.offset(skip).limit(limit).all()


@router.get("/movements", response_model=list[StockMovementResponse])
def list_movements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    product_id: UUID | None = None,
    warehouse_id: UUID | None = None,
    skip: int = 0,
    limit: int = 200,
) -> Any:
    query = db.query(InventoryStockMovement).order_by(InventoryStockMovement.movement_date.desc())
    if product_id:
        query = query.filter(InventoryStockMovement.product_id == product_id)
    if warehouse_id:
        query = query.filter(InventoryStockMovement.warehouse_id == warehouse_id)
    return query.offset(skip).limit(limit).all()


@router.post("/adjustments", response_model=StockMovementResponse, status_code=status.HTTP_201_CREATED)
def create_adjustment(
    adjustment_in: StockAdjustmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    """Manual stock correction (count adjustment, waste, etc). Posts
    immediately - there is no draft/approval step for adjustments."""
    product = (
        db.query(Product)
        .filter(Product.id == adjustment_in.product_id, Product.is_deleted == False)
        .first()
    )
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    warehouse = (
        db.query(Warehouse)
        .filter(Warehouse.id == adjustment_in.warehouse_id, Warehouse.is_deleted == False)
        .first()
    )
    if not warehouse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Warehouse not found")

    movement = InventoryStockMovement(
        product_id=adjustment_in.product_id,
        warehouse_id=adjustment_in.warehouse_id,
        movement_type=adjustment_in.movement_type,
        quantity=adjustment_in.quantity,
        unit_cost=adjustment_in.unit_cost,
        reference_type="ADJUSTMENT",
        notes=adjustment_in.notes,
        created_by=current_user.id,
    )
    db.add(movement)
    db.flush()

    StockEngine().update_balance_from_movement(db, movement)

    db.commit()
    db.refresh(movement)
    return movement
