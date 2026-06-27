from __future__ import annotations

from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import ERPBaseModel


class TenantCompany(ERPBaseModel):
    __tablename__ = "tenant_companies"

    name: Mapped[str] = mapped_column(String(255))

    email: Mapped[str] = mapped_column(String(255))

    plan: Mapped[str] = mapped_column(String(50), default="FREE")

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
