from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_superuser, get_current_user
from app.core.database import get_db
from app.models.supplier import Supplier
from app.models.user import User
from app.schemas.supplier import SupplierCreate, SupplierResponse, SupplierUpdate

router = APIRouter()


@router.get("/", response_model=list[SupplierResponse])
def list_suppliers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    return (
        db.query(Supplier)
        .filter(Supplier.company_id == current_user.company_id, Supplier.is_deleted == False)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(
    supplier_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    supplier = (
        db.query(Supplier)
        .filter(Supplier.id == supplier_id, Supplier.is_deleted == False)
        .first()
    )
    if not supplier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")
    return supplier


@router.post("/", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(
    supplier_in: SupplierCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    supplier = Supplier(**supplier_in.model_dump(), created_by=current_user.id)
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier


@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_supplier(
    supplier_id: UUID,
    supplier_in: SupplierUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    supplier = (
        db.query(Supplier)
        .filter(Supplier.id == supplier_id, Supplier.is_deleted == False)
        .first()
    )
    if not supplier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")

    for field, value in supplier_in.model_dump(exclude_unset=True).items():
        setattr(supplier, field, value)
    supplier.updated_by = current_user.id

    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier


@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(
    supplier_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> None:
    from datetime import datetime, timezone

    supplier = (
        db.query(Supplier)
        .filter(Supplier.id == supplier_id, Supplier.is_deleted == False)
        .first()
    )
    if not supplier:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found")

    supplier.is_deleted = True
    supplier.deleted_at = datetime.now(timezone.utc)
    supplier.deleted_by = current_user.id
    supplier.is_active = False
    db.add(supplier)
    db.commit()
    return None
