from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, Numeric, DateTime, String, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ERPBaseModel


class SalesPayment(ERPBaseModel):
    __tablename__ = "sales_payments"

    __table_args__ = (
        Index("ix_sales_payments_invoice_id", "invoice_id"),
    )

    invoice_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sales_invoices.id"),
        nullable=False,
    )

    payment_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )

    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    method: Mapped[str] = mapped_column(
        String(30),
        default="CASH",  # CASH / CARD / WALLET / BANK
    )

    reference: Mapped[str | None] = mapped_column(String(100))

    invoice = relationship("SalesInvoice", back_populates="payments")
