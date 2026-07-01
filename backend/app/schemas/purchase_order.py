from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PurchaseOrderItemCreate(BaseModel):
    product_id: UUID
    quantity: float = Field(gt=0)
    unit_cost: float = Field(ge=0)
    notes: str | None = None


class PurchaseOrderItemResponse(BaseModel):
    id: UUID
    product_id: UUID
    quantity: float
    unit_cost: float
    total: float
    received_quantity: float
    notes: str | None

    model_config = ConfigDict(from_attributes=True)


class PurchaseOrderCreate(BaseModel):
    supplier_id: UUID
    branch_id: UUID
    discount: float = Field(default=0, ge=0)
    tax: float = Field(default=0, ge=0)
    items: list[PurchaseOrderItemCreate]

    @model_validator(mode="after")
    def must_have_items(self):
        if not self.items:
            raise ValueError("Purchase order must have at least one item")
        return self


class PurchaseOrderUpdate(BaseModel):
    """Only allowed while status is DRAFT - see endpoint for the check."""

    supplier_id: UUID | None = None
    discount: float | None = Field(default=None, ge=0)
    tax: float | None = Field(default=None, ge=0)
    items: list[PurchaseOrderItemCreate] | None = None


class PurchaseOrderResponse(BaseModel):
    id: UUID
    order_number: str
    order_date: datetime
    supplier_id: UUID
    branch_id: UUID
    status: str
    subtotal: float
    discount: float
    tax: float
    total: float
    is_posted: bool
    items: list[PurchaseOrderItemResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
