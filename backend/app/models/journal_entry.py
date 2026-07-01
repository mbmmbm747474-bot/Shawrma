from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey, Boolean, Index
from app.models.types import GUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ERPBaseModel


class JournalEntry(ERPBaseModel):
    __tablename__ = "journal_entries"

    __table_args__ = (
        Index("ix_journal_entries_number", "entry_number"),
        Index("ix_journal_entries_date", "entry_date"),
    )

    entry_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    entry_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(String(255))

    is_posted: Mapped[bool] = mapped_column(Boolean, default=False)

    source_type: Mapped[str | None] = mapped_column(String(50))  # SALES / PURCHASE / MANUAL

    source_id: Mapped[uuid.UUID | None] = mapped_column(GUID())

    branch_id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        ForeignKey("branches.id"),
        nullable=False,
    )

    items = relationship(
        "JournalItem",
        back_populates="entry",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
