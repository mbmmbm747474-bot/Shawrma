from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, Numeric, String, Index
from app.models.types import GUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ERPBaseModel


class RecipeItem(ERPBaseModel):
    __tablename__ = "recipe_items"

    __table_args__ = (
        Index("ix_recipe_items_recipe_id", "recipe_id"),
        Index("ix_recipe_items_product_id", "product_id"),
    )

    recipe_id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        ForeignKey("recipes.id"),
        nullable=False,
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        ForeignKey("products.id"),
        nullable=False,
    )

    quantity: Mapped[float] = mapped_column(Numeric(12, 3), nullable=False)

    unit_cost: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    total_cost: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    unit: Mapped[str | None] = mapped_column(String(20))  # kg / g / pcs / liter

    recipe = relationship("Recipe", back_populates="items")
