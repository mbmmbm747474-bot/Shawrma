import uuid

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class CostCenter(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "cost_centers"

    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False
    )
    
    branch_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("branches.id"), nullable=True
    )
    
    name: Mapped[str] = mapped_column(
        String(200), nullable=False
    )
    
    code: Mapped[str | None] = mapped_column(
        String(50), nullable=True
    )
    
    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("cost_centers.id"), nullable=True
    )
    
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )

    # Relationships
    parent = relationship("CostCenter", remote_side="[CostCenter.id]")
    company = relationship("Company")
    branch = relationship("Branch")

    def __repr__(self) -> str:
        return f"<CostCenter(name='{self.name}', code='{self.code}')>"
