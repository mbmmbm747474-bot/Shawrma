import uuid
from datetime import time

from sqlalchemy import Boolean, ForeignKey, String, Text, Time
from app.models.types import GUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin


class Branch(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "branches"

    company_id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        ForeignKey("companies.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    code: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    email: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    manager_name: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    tax_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    opening_time: Mapped[time | None] = mapped_column(
        Time,
        nullable=True,
    )

    closing_time: Mapped[time | None] = mapped_column(
        Time,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Relationships
    company = relationship(
        "Company",
        back_populates="branches",
    )

    users = relationship(
        "User",
        back_populates="branch",
        foreign_keys="User.branch_id",
    )

    def __repr__(self) -> str:
        return f"<Branch(name='{self.name}', id='{self.id}')>"
