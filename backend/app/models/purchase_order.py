from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import String, ForeignKey, Numeric, DateTime, Boolean, Index
from app.models.types import GUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ERPBaseModel


class PurchaseOrder(ERPBaseModel):
    __tablename__ = "purchase_orders"

    __table_args__ = (
        Index("ix_purchase_orders_number", "order_number"),
        Index("ix_purchase_orders_supplier_id", "supplier_id"),
        Index("ix_purchase_orders_branch_id", "branch_id"),
    )

    order_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    order_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    supplier_id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        ForeignKey("suppliers.id"),
        nullable=False,
    )

    branch_id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        ForeignKey("branches.id"),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="DRAFT",  # DRAFT / APPROVED / RECEIVED / CANCELLED
    )

    subtotal: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    discount: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    tax: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    total: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    is_posted: Mapped[bool] = mapped_column(Boolean, default=False)

    items = relationship(
        "PurchaseOrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
