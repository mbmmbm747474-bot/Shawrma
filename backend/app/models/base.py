from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from app.models.types import GUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class UUIDMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        primary_key=True,
        default=uuid.uuid4,
    )


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class AuditMixin:

    created_by: Mapped[uuid.UUID | None] = mapped_column(
        GUID(),
        ForeignKey("users.id"),
        nullable=True,
    )

    updated_by: Mapped[uuid.UUID | None] = mapped_column(
        GUID(),
        ForeignKey("users.id"),
        nullable=True,
    )


class SoftDeleteMixin:

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    deleted_by: Mapped[uuid.UUID | None] = mapped_column(
        GUID(),
        ForeignKey("users.id"),
        nullable=True,
    )


class ERPBaseModel(
    Base,
    UUIDMixin,
    TimestampMixin,
    AuditMixin,
    SoftDeleteMixin,
):
    __abstract__ = True

    # Nullable for now: no tenant-resolution middleware exists yet in this
    # milestone. When multi-tenant SaaS routing is built, this should
    # become non-nullable and populated automatically per request.
    tenant_id: Mapped[str | None] = mapped_column(String(50), index=True, nullable=True)
