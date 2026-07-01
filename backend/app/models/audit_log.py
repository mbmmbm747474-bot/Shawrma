import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from app.models.types import GUID, PortableJSON
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin


class AuditLog(Base, UUIDMixin):
    __tablename__ = "audit_logs"

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("users.id"), nullable=True
    )
    
    company_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("companies.id"), nullable=True
    )
    
    branch_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("branches.id"), nullable=True
    )
    
    table_name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )
    
    record_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), nullable=True
    )
    
    action: Mapped[str] = mapped_column(
        String(50), nullable=False
    )
    
    old_data: Mapped[dict | None] = mapped_column(
        PortableJSON, nullable=True
    )
    
    new_data: Mapped[dict | None] = mapped_column(
        PortableJSON, nullable=True
    )
    
    ip_address: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        return f"<AuditLog(action='{self.action}', table='{self.table_name}')>"
