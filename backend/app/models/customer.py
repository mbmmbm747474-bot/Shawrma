from __future__ import annotations

import uuid

from sqlalchemy import String, Boolean, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import ERPBaseModel


class Customer(ERPBaseModel):
    __tablename__ = "customers"

    __table_args__ = (
        Index("ix_customers_name", "name"),
        Index("ix_customers_phone", "phone"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    phone: Mapped[str | None] = mapped_column(String(30))

    email: Mapped[str | None] = mapped_column(String(255))

    address: Mapped[str | None] = mapped_column(String(500))

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
