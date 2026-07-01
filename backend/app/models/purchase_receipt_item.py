from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, Numeric, String, Index
from app.models.types import GUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ERPBaseModel


class PurchaseReceiptItem(ERPBaseModel):
    __tablename__ = "purchase_receipt_items"

    __table_args__ = (
        Index("ix_receipt_items_receipt_id", "receipt_id"),
        Index("ix_receipt_items_product_id", "product_id"),
    )

    receipt_id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        ForeignKey("purchase_receipts.id"),
        nullable=False,
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        ForeignKey("products.id"),
        nullable=False,
    )

    quantity: Mapped[float] = mapped_column(Numeric(12, 3), nullable=False)

    unit_cost: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    total: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    receipt = relationship("PurchaseReceipt", back_populates="items")
