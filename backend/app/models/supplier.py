from __future__ import annotations

import uuid

from sqlalchemy import String, Boolean, ForeignKey, Index
from app.models.types import GUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ERPBaseModel


class Supplier(ERPBaseModel):
    __tablename__ = "suppliers"

    __table_args__ = (
        Index("ix_suppliers_name", "name"),
        Index("ix_suppliers_company_id", "company_id"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    phone: Mapped[str | None] = mapped_column(String(30))

    email: Mapped[str | None] = mapped_column(String(255))

    address: Mapped[str | None] = mapped_column(String(500))

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    company_id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        ForeignKey("companies.id"),
        nullable=False,
    )
