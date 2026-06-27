from __future__ import annotations

import uuid

from sqlalchemy import String, Boolean, ForeignKey, Numeric, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ERPBaseModel


class Product(ERPBaseModel):
    __tablename__ = "products"

    __table_args__ = (
        Index("ix_products_name", "name"),
        Index("ix_products_sku", "sku"),
        Index("ix_products_category_id", "category_id"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    sku: Mapped[str | None] = mapped_column(String(100), unique=True)

    barcode: Mapped[str | None] = mapped_column(String(100))

    sale_price: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    cost_price: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("product_categories.id"),
        nullable=False,
    )

    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("companies.id"),
        nullable=False,
    )

    category = relationship("ProductCategory", back_populates="products")
