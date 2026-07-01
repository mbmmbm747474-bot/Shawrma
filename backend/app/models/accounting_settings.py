from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, String
from app.models.types import GUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import ERPBaseModel


class AccountingSettings(ERPBaseModel):
    __tablename__ = "accounting_settings"

    company_id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        ForeignKey("companies.id"),
        nullable=False,
        unique=True,
    )

    cash_account_id: Mapped[uuid.UUID | None] = mapped_column(GUID())

    sales_account_id: Mapped[uuid.UUID | None] = mapped_column(GUID())

    inventory_account_id: Mapped[uuid.UUID | None] = mapped_column(GUID())

    cost_of_goods_sold_account_id: Mapped[uuid.UUID | None] = mapped_column(GUID())

    tax_account_id: Mapped[uuid.UUID | None] = mapped_column(GUID())
