from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, Numeric, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import ERPBaseModel


class RecipeCostSnapshot(ERPBaseModel):
    __tablename__ = "recipe_cost_snapshots"

    __table_args__ = (
        Index("ix_recipe_snapshots_recipe_id", "recipe_id"),
    )

    recipe_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("recipes.id"),
        nullable=False,
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id"),
        nullable=False,
    )

    total_cost: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    cost_per_unit: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    food_cost_percentage: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    snapshot_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )
