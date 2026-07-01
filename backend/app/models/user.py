from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    String,
)

from app.models.types import GUID
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base import ERPBaseModel


class User(ERPBaseModel):
    __tablename__ = "users"

    __table_args__ = (
        Index("ix_users_username", "username"),
        Index("ix_users_email", "email"),
        Index("ix_users_branch_id", "branch_id"),
    )

    employee_no: Mapped[str | None] = mapped_column(
        String(30),
        unique=True,
        nullable=True,
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    mobile: Mapped[str | None] = mapped_column(
        String(30),
    )

    language: Mapped[str] = mapped_column(
        String(10),
        default="ar",
    )

    timezone: Mapped[str] = mapped_column(
        String(50),
        default="Africa/Cairo",
    )

    avatar: Mapped[str | None] = mapped_column(
        String(500),
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    must_change_password: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    company_id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        ForeignKey("companies.id"),
        nullable=False,
    )

    branch_id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        ForeignKey("branches.id"),
        nullable=False,
    )

    company = relationship(
        "Company",
        back_populates="users",
        foreign_keys=[company_id],
    )

    branch = relationship(
        "Branch",
        back_populates="users",
        foreign_keys=[branch_id],
    )

    roles = relationship(
        "Role",
        secondary="user_roles",
        primaryjoin="User.id == UserRole.user_id",
        secondaryjoin="UserRole.role_id == Role.id",
        back_populates="users",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return (
            f"<User("
            f"username='{self.username}', "
            f"email='{self.email}')>"
        )
