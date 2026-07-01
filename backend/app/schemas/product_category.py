from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProductCategoryBase(BaseModel):
    name: str
    description: str | None = None
    is_active: bool = True


class ProductCategoryCreate(ProductCategoryBase):
    company_id: UUID


class ProductCategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class ProductCategoryResponse(ProductCategoryBase):
    id: UUID
    company_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
