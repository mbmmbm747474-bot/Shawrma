from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_superuser, get_current_user
from app.core.database import get_db
from app.models.warehouse import Warehouse
from app.models.user import User
from app.schemas.warehouse import WarehouseCreate, WarehouseResponse, WarehouseUpdate

router = APIRouter()


@router.get("/", response_model=list[WarehouseResponse])
def list_warehouses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    branch_id: UUID | None = None,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    query = db.query(Warehouse).filter(Warehouse.is_deleted == False)
    if branch_id:
        query = query.filter(Warehouse.branch_id == branch_id)
    return query.offset(skip).limit(limit).all()


@router.get("/{warehouse_id}", response_model=WarehouseResponse)
def get_warehouse(
    warehouse_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    warehouse = (
        db.query(Warehouse)
        .filter(Warehouse.id == warehouse_id, Warehouse.is_deleted == False)
        .first()
    )
    if not warehouse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Warehouse not found")
    return warehouse


@router.post("/", response_model=WarehouseResponse, status_code=status.HTTP_201_CREATED)
def create_warehouse(
    warehouse_in: WarehouseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    warehouse = Warehouse(**warehouse_in.model_dump(), created_by=current_user.id)
    db.add(warehouse)
    db.commit()
    db.refresh(warehouse)
    return warehouse


@router.put("/{warehouse_id}", response_model=WarehouseResponse)
def update_warehouse(
    warehouse_id: UUID,
    warehouse_in: WarehouseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    warehouse = (
        db.query(Warehouse)
        .filter(Warehouse.id == warehouse_id, Warehouse.is_deleted == False)
        .first()
    )
    if not warehouse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Warehouse not found")

    for field, value in warehouse_in.model_dump(exclude_unset=True).items():
        setattr(warehouse, field, value)
    warehouse.updated_by = current_user.id

    db.add(warehouse)
    db.commit()
    db.refresh(warehouse)
    return warehouse


@router.delete("/{warehouse_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_warehouse(
    warehouse_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> None:
    from datetime import datetime, timezone

    warehouse = (
        db.query(Warehouse)
        .filter(Warehouse.id == warehouse_id, Warehouse.is_deleted == False)
        .first()
    )
    if not warehouse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Warehouse not found")

    warehouse.is_deleted = True
    warehouse.deleted_at = datetime.now(timezone.utc)
    warehouse.deleted_by = current_user.id
    warehouse.is_active = False
    db.add(warehouse)
    db.commit()
    return None
