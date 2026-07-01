import uuid

from sqlalchemy import Boolean, ForeignKey, String, Text, UniqueConstraint
from app.models.types import GUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Permission(Base, UUIDMixin):
    __tablename__ = "permissions"

    module: Mapped[str] = mapped_column(String(100), nullable=False)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint("module", "action", name="uq_permissions_module_action"),
    )

    def __repr__(self) -> str:
        return f"<Permission(module='{self.module}', action='{self.action}')>"


class RolePermission(Base, UUIDMixin):
    __tablename__ = "role_permissions"

    role_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False
    )
    permission_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False
    )

    __table_args__ = (
        UniqueConstraint("role_id", "permission_id", name="uq_role_permissions_role_permission"),
    )


class UserRole(Base, UUIDMixin):
    __tablename__ = "user_roles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    role_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False
    )
    branch_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(), ForeignKey("branches.id"), nullable=True
    )

    __table_args__ = (
        UniqueConstraint("user_id", "role_id", "branch_id", name="uq_user_roles_user_role_branch"),
    )


class Role(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "roles"

    company_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("companies.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_system: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    permissions = relationship(
        "Permission",
        secondary="role_permissions",
        lazy="selectin"
    )
    users = relationship(
        "User",
        secondary="user_roles",
        primaryjoin="Role.id == UserRole.role_id",
        secondaryjoin="UserRole.user_id == User.id",
        back_populates="roles"
    )

    def __repr__(self) -> str:
        return f"<Role(name='{self.name}', company_id='{self.company_id}')>"
