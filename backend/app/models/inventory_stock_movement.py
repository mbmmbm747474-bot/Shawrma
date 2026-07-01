from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Numeric, String
from app.models.types import GUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import ERPBaseModel


class InventoryStockMovement(ERPBaseModel):
    __tablename__ = "inventory_stock_movements"

    __table_args__ = (
        Index("ix_stock_movements_product_id", "product_id"),
        Index("ix_stock_movements_warehouse_id", "warehouse_id"),
        Index("ix_stock_movements_reference", "reference_type", "reference_id"),
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        ForeignKey("products.id"),
        nullable=False,
    )

    warehouse_id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        ForeignKey("warehouses.id"),
        nullable=False,
    )

    movement_type: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )  # IN / OUT

    quantity: Mapped[float] = mapped_column(Numeric(12, 3), nullable=False)

    unit_cost: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)

    movement_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    reference_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )  # SALES / PURCHASE / RECIPE_CONSUMPTION / ADJUSTMENT / TRANSFER

    reference_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(),
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(String(255), nullable=True)
