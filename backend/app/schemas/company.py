from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class CompanyBase(BaseModel):
    name: str
    legal_name: str | None = None
    tax_number: str | None = None
    commercial_register: str | None = None
    address: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    currency: str = "EGP"
    is_active: bool = True


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: str | None = None
    legal_name: str | None = None
    tax_number: str | None = None
    commercial_register: str | None = None
    address: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    currency: str | None = None
    is_active: bool | None = None


class CompanyResponse(CompanyBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
