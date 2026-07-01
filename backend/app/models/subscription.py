from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import String, ForeignKey, DateTime, Boolean
from app.models.types import GUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import ERPBaseModel


class Subscription(ERPBaseModel):
    __tablename__ = "subscriptions"

    company_id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        ForeignKey("tenant_companies.id")
    )

    plan: Mapped[str] = mapped_column(String(50))  # BASIC / PRO / ENTERPRISE

    start_date: Mapped[datetime] = mapped_column(DateTime)

    end_date: Mapped[datetime] = mapped_column(DateTime)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
