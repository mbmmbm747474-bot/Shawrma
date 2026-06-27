from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, Numeric, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import ERPBaseModel


class InventoryBalance(ERPBaseModel):
    __tablename__ = "inventory_balances"

    __table_args__ = (
        Index("ix_inventory_balance_product_warehouse", "product_id", "warehouse_id", unique=True),
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id"),
        nullable=False,
    )

    warehouse_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("warehouses.id"),
        nullable=False,
    )

    quantity_on_hand: Mapped[float] = mapped_column(Numeric(12, 3), default=0)

    reserved_quantity: Mapped[float] = mapped_column(Numeric(12, 3), default=0)

    available_quantity: Mapped[float] = mapped_column(Numeric(12, 3), default=0)

    average_cost: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
