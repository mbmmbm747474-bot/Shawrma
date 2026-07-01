from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class InventoryBalanceResponse(BaseModel):
    id: UUID
    product_id: UUID
    warehouse_id: UUID
    quantity_on_hand: float
    reserved_quantity: float
    available_quantity: float
    average_cost: float
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StockMovementResponse(BaseModel):
    id: UUID
    product_id: UUID
    warehouse_id: UUID
    movement_type: str
    quantity: float
    unit_cost: float | None
    movement_date: datetime
    reference_type: str | None
    reference_id: UUID | None
    notes: str | None

    model_config = ConfigDict(from_attributes=True)


class StockAdjustmentCreate(BaseModel):
    """Manual stock adjustment - the only way to create a movement directly
    rather than through a goods receipt. Lets you correct counts, record
    waste, etc. movement_type must be IN or OUT."""

    product_id: UUID
    warehouse_id: UUID
    movement_type: str = Field(pattern="^(IN|OUT)$")
    quantity: float = Field(gt=0)
    unit_cost: float | None = Field(default=None, ge=0)
    notes: str | None = None
