from __future__ import annotations

import uuid

from sqlalchemy import String, Boolean, Index
from app.models.types import GUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ERPBaseModel


class Company(ERPBaseModel):
    __tablename__ = "companies"

    __table_args__ = (
        Index("ix_companies_name", "name"),
        Index("ix_companies_tax_number", "tax_number"),
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    legal_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    tax_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    commercial_register: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        default="EGP",
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    users = relationship(
        "User",
        back_populates="company",
        foreign_keys="User.company_id",
        lazy="selectin",
    )

    branches = relationship(
        "Branch",
        back_populates="company",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Company(name='{self.name}')>"
