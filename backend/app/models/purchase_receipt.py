from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import String, ForeignKey, DateTime, Numeric, Boolean, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ERPBaseModel


class PurchaseReceipt(ERPBaseModel):
    __tablename__ = "purchase_receipts"

    __table_args__ = (
        Index("ix_purchase_receipts_number", "receipt_number"),
        Index("ix_purchase_receipts_order_id", "order_id"),
    )

    receipt_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    receipt_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )

    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("purchase_orders.id"),
        nullable=False,
    )

    supplier_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("suppliers.id"),
        nullable=False,
    )

    branch_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("branches.id"),
        nullable=False,
    )

    total: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    is_posted: Mapped[bool] = mapped_column(Boolean, default=False)

    items = relationship(
        "PurchaseReceiptItem",
        back_populates="receipt",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
