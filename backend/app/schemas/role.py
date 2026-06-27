from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PermissionResponse(BaseModel):
    id: UUID
    module: str
    action: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)


class RoleBase(BaseModel):
    name: str
    description: str | None = None
    is_active: bool = True


class RoleCreate(RoleBase):
    company_id: UUID
    permission_ids: list[UUID] = []


class RoleUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None
    permission_ids: list[UUID] | None = None


class RoleResponse(RoleBase):
    id: UUID
    company_id: UUID
    is_system: bool
    created_at: datetime
    permissions: list[PermissionResponse] = []

    model_config = ConfigDict(from_attributes=True)


class AssignRoleRequest(BaseModel):
    user_id: UUID
    role_id: UUID
    branch_id: UUID | None = None
