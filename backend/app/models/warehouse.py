from __future__ import annotations

import uuid

from sqlalchemy import String, Boolean, ForeignKey, Index
from app.models.types import GUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import ERPBaseModel


class Warehouse(ERPBaseModel):
    __tablename__ = "warehouses"

    __table_args__ = (
        Index("ix_warehouses_name", "name"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    branch_id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        ForeignKey("branches.id"),
        nullable=False,
    )
