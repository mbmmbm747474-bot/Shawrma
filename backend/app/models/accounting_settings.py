from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import ERPBaseModel


class AccountingSettings(ERPBaseModel):
    __tablename__ = "accounting_settings"

    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("companies.id"),
        nullable=False,
        unique=True,
    )

    cash_account_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))

    sales_account_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))

    inventory_account_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))

    cost_of_goods_sold_account_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))

    tax_account_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
