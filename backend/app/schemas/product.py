from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str
    sku: str | None = None
    barcode: str | None = None
    sale_price: float = Field(default=0, ge=0)
    cost_price: float = Field(default=0, ge=0)
    is_active: bool = True


class ProductCreate(ProductBase):
    category_id: UUID
    company_id: UUID


class ProductUpdate(BaseModel):
    name: str | None = None
    sku: str | None = None
    barcode: str | None = None
    sale_price: float | None = Field(default=None, ge=0)
    cost_price: float | None = Field(default=None, ge=0)
    is_active: bool | None = None
    category_id: UUID | None = None


class ProductResponse(ProductBase):
    id: UUID
    category_id: UUID
    company_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
