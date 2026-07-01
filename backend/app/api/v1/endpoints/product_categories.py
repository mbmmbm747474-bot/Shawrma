from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_superuser, get_current_user
from app.core.database import get_db
from app.models.product_category import ProductCategory
from app.models.user import User
from app.schemas.product_category import (
    ProductCategoryCreate,
    ProductCategoryResponse,
    ProductCategoryUpdate,
)

router = APIRouter()


@router.get("/", response_model=list[ProductCategoryResponse])
def list_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    return (
        db.query(ProductCategory)
        .filter(ProductCategory.company_id == current_user.company_id, ProductCategory.is_deleted == False)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/{category_id}", response_model=ProductCategoryResponse)
def get_category(
    category_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    category = (
        db.query(ProductCategory)
        .filter(ProductCategory.id == category_id, ProductCategory.is_deleted == False)
        .first()
    )
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


@router.post("/", response_model=ProductCategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category_in: ProductCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    category = ProductCategory(**category_in.model_dump(), created_by=current_user.id)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.put("/{category_id}", response_model=ProductCategoryResponse)
def update_category(
    category_id: UUID,
    category_in: ProductCategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    category = (
        db.query(ProductCategory)
        .filter(ProductCategory.id == category_id, ProductCategory.is_deleted == False)
        .first()
    )
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    for field, value in category_in.model_dump(exclude_unset=True).items():
        setattr(category, field, value)
    category.updated_by = current_user.id

    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> None:
    from datetime import datetime, timezone

    category = (
        db.query(ProductCategory)
        .filter(ProductCategory.id == category_id, ProductCategory.is_deleted == False)
        .first()
    )
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    category.is_deleted = True
    category.deleted_at = datetime.now(timezone.utc)
    category.deleted_by = current_user.id
    category.is_active = False
    db.add(category)
    db.commit()
    return None
