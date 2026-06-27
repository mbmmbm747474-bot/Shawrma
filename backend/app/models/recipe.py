from __future__ import annotations

import uuid

from sqlalchemy import String, Boolean, ForeignKey, Numeric, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ERPBaseModel


class Recipe(ERPBaseModel):
    __tablename__ = "recipes"

    __table_args__ = (
        Index("ix_recipes_product_id", "product_id"),
        Index("ix_recipes_company_id", "company_id"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id"),
        nullable=False,
        unique=True,
    )

    yield_quantity: Mapped[float] = mapped_column(
        Numeric(12, 3),
        default=1,
        nullable=False,
    )

    total_cost: Mapped[float] = mapped_column(
        Numeric(12, 2),
        default=0,
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("companies.id"),
        nullable=False,
    )

    items = relationship(
        "RecipeItem",
        back_populates="recipe",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
