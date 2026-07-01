from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class SupplierBase(BaseModel):
    name: str
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None
    is_active: bool = True


class SupplierCreate(SupplierBase):
    company_id: UUID


class SupplierUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None
    is_active: bool | None = None


class SupplierResponse(SupplierBase):
    id: UUID
    company_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
