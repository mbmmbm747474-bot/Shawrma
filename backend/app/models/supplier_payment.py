from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import String, ForeignKey, Numeric, DateTime, Index
from app.models.types import GUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import ERPBaseModel


class SupplierPayment(ERPBaseModel):
    __tablename__ = "supplier_payments"

    __table_args__ = (
        Index("ix_supplier_payments_supplier_id", "supplier_id"),
    )

    supplier_id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        ForeignKey("suppliers.id"),
        nullable=False,
    )

    payment_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )

    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    method: Mapped[str] = mapped_column(
        String(30),
        default="CASH",
    )

    reference: Mapped[str | None] = mapped_column(String(100))
