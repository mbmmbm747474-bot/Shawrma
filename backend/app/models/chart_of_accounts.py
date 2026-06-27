from __future__ import annotations

import uuid

from sqlalchemy import String, Boolean, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ERPBaseModel


class AccountType(str):
    ASSET = "ASSET"
    LIABILITY = "LIABILITY"
    EQUITY = "EQUITY"
    REVENUE = "REVENUE"
    EXPENSE = "EXPENSE"


class ChartOfAccount(ERPBaseModel):
    __tablename__ = "chart_of_accounts"

    __table_args__ = (
        Index("ix_accounts_code", "code"),
        Index("ix_accounts_parent_id", "parent_id"),
    )

    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    account_type: Mapped[str] = mapped_column(String(20), nullable=False)

    is_postable: Mapped[bool] = mapped_column(Boolean, default=True)

    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("chart_of_accounts.id"),
        nullable=True,
    )

    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("companies.id"),
        nullable=False,
    )

    children = relationship("ChartOfAccount", remote_side="ChartOfAccount.id")
