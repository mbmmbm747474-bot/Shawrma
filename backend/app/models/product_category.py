from __future__ import annotations

import uuid

from sqlalchemy import String, Boolean, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ERPBaseModel


class ProductCategory(ERPBaseModel):
    __tablename__ = "product_categories"

    __table_args__ = (
        Index("ix_product_categories_name", "name"),
        Index("ix_product_categories_company_id", "company_id"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    description: Mapped[str | None] = mapped_column(String(500))

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("companies.id"),
        nullable=False,
    )

    products = relationship("Product", back_populates="category")
