from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey, Numeric, String, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ERPBaseModel


class JournalItem(ERPBaseModel):
    __tablename__ = "journal_items"

    __table_args__ = (
        Index("ix_journal_items_entry_id", "entry_id"),
        Index("ix_journal_items_account_id", "account_id"),
    )

    entry_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("journal_entries.id"),
        nullable=False,
    )

    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("chart_of_accounts.id"),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(String(255))

    debit: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    credit: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    entry = relationship("JournalEntry", back_populates="items")
