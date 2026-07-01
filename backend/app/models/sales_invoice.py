from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import String, ForeignKey, Numeric, DateTime, Boolean, Index
from app.models.types import GUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ERPBaseModel


class SalesInvoice(ERPBaseModel):
    __tablename__ = "sales_invoices"

    __table_args__ = (
        Index("ix_sales_invoices_number", "invoice_number"),
        Index("ix_sales_invoices_customer_id", "customer_id"),
        Index("ix_sales_invoices_branch_id", "branch_id"),
    )

    invoice_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    invoice_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    customer_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(),
        ForeignKey("customers.id"),
        nullable=True,
    )

    branch_id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        ForeignKey("branches.id"),
        nullable=False,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        ForeignKey("users.id"),
        nullable=False,
    )

    subtotal: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    discount: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    tax: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    total: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    paid_amount: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    remaining_amount: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    status: Mapped[str] = mapped_column(
        String(20),
        default="DRAFT",
    )

    is_posted: Mapped[bool] = mapped_column(Boolean, default=False)

    items = relationship(
        "SalesInvoiceItem",
        back_populates="invoice",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    payments = relationship(
        "SalesPayment",
        back_populates="invoice",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
