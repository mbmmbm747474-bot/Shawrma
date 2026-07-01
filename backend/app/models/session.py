import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from app.models.types import GUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin


class UserSession(Base, UUIDMixin):
    __tablename__ = "user_sessions"

    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    
    refresh_token: Mapped[str] = mapped_column(
        Text, unique=True, nullable=False
    )
    
    ip_address: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )
    
    user_agent: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )
    
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationship
    user = relationship("User")

    def __repr__(self) -> str:
        return f"<UserSession(user_id='{self.user_id}')>"
