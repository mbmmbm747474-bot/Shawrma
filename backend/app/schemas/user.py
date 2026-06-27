from uuid import UUID
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    mobile: str | None = None
    language: str = "ar"
    timezone: str = "Africa/Cairo"
    avatar: str | None = None
    is_active: bool = True
    is_superuser: bool = False

class UserCreate(UserBase):
    password: str
    company_id: UUID
    branch_id: UUID

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    full_name: str | None = None
    mobile: str | None = None
    password: str | None = None
    language: str | None = None
    timezone: str | None = None
    avatar: str | None = None
    is_active: bool | None = None

class UserResponse(UserBase):
    id: UUID
    company_id: UUID
    branch_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
