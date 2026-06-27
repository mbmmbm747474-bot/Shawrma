from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, Numeric, Index, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ERPBaseModel


class SalesInvoiceItem(ERPBaseModel):
    __tablename__ = "sales_invoice_items"

    __table_args__ = (
        Index("ix_sales_invoice_items_invoice_id", "invoice_id"),
        Index("ix_sales_invoice_items_product_id", "product_id"),
    )

    invoice_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sales_invoices.id"),
        nullable=False,
    )

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id"),
        nullable=False,
    )

    quantity: Mapped[float] = mapped_column(Numeric(12, 3), nullable=False)

    unit_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    cost_price: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    discount: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    total: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)

    notes: Mapped[str | None] = mapped_column(String(255))

    invoice = relationship("SalesInvoice", back_populates="items")
