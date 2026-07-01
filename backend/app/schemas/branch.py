from datetime import time, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class BranchBase(BaseModel):
    name: str
    code: str | None = None
    address: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    manager_name: str | None = None
    tax_number: str | None = None
    opening_time: time | None = None
    closing_time: time | None = None
    is_active: bool = True


class BranchCreate(BranchBase):
    company_id: UUID


class BranchUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    address: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    manager_name: str | None = None
    tax_number: str | None = None
    opening_time: time | None = None
    closing_time: time | None = None
    is_active: bool | None = None


class BranchResponse(BranchBase):
    id: UUID
    company_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
