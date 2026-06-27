from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, Numeric, String, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ERPBaseModel


class PurchaseOrderItem(ERPBaseModel):
    __tablename__ = "purchase_order_items"

    __table_args__ = (
        Index("ix_purchase_items_order_id", "order_id"),
        Index("ix_purchase_items_product_id", "product_id"),
    )

    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("purchase_orders.id"),
        nullable=False,
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id"),
        nullable=False,
    )

    quantity: Mapped[float] = mapped_column(Numeric(12, 3), nullable=False)

    unit_cost: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    total: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    received_quantity: Mapped[float] = mapped_column(Numeric(12, 3), default=0)

    notes: Mapped[str | None] = mapped_column(String(255))

    order = relationship("PurchaseOrder", back_populates="items")
