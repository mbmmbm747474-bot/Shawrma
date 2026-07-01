from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class WarehouseBase(BaseModel):
    name: str
    is_active: bool = True


class WarehouseCreate(WarehouseBase):
    branch_id: UUID


class WarehouseUpdate(BaseModel):
    name: str | None = None
    is_active: bool | None = None


class WarehouseResponse(WarehouseBase):
    id: UUID
    branch_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
