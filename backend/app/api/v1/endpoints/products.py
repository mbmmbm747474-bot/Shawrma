from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_superuser, get_current_user
from app.core.database import get_db
from app.models.product import Product
from app.models.user import User
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter()


@router.get("/", response_model=list[ProductResponse])
def list_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    category_id: UUID | None = None,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    query = db.query(Product).filter(
        Product.company_id == current_user.company_id, Product.is_deleted == False
    )
    if category_id:
        query = query.filter(Product.category_id == category_id)
    return query.offset(skip).limit(limit).all()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    product = (
        db.query(Product)
        .filter(Product.id == product_id, Product.is_deleted == False)
        .first()
    )
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    if product_in.sku:
        existing = db.query(Product).filter(Product.sku == product_in.sku).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A product with this SKU already exists",
            )

    product = Product(**product_in.model_dump(), created_by=current_user.id)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: UUID,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    product = (
        db.query(Product)
        .filter(Product.id == product_id, Product.is_deleted == False)
        .first()
    )
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    update_data = product_in.model_dump(exclude_unset=True)
    if "sku" in update_data and update_data["sku"] and update_data["sku"] != product.sku:
        existing = db.query(Product).filter(Product.sku == update_data["sku"]).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A product with this SKU already exists",
            )

    for field, value in update_data.items():
        setattr(product, field, value)
    product.updated_by = current_user.id

    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> None:
    from datetime import datetime, timezone

    product = (
        db.query(Product)
        .filter(Product.id == product_id, Product.is_deleted == False)
        .first()
    )
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    product.is_deleted = True
    product.deleted_at = datetime.now(timezone.utc)
    product.deleted_by = current_user.id
    product.is_active = False
    db.add(product)
    db.commit()
    return None
