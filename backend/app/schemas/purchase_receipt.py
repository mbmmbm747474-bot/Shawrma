from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PurchaseReceiptItemCreate(BaseModel):
    product_id: UUID
    quantity: float = Field(gt=0)
    unit_cost: float = Field(ge=0)


class PurchaseReceiptItemResponse(BaseModel):
    id: UUID
    product_id: UUID
    quantity: float
    unit_cost: float
    total: float

    model_config = ConfigDict(from_attributes=True)


class PurchaseReceiptCreate(BaseModel):
    order_id: UUID
    warehouse_id: UUID
    items: list[PurchaseReceiptItemCreate]

    @model_validator(mode="after")
    def must_have_items(self):
        if not self.items:
            raise ValueError("Goods receipt must have at least one item")
        return self


class PurchaseReceiptResponse(BaseModel):
    id: UUID
    receipt_number: str
    receipt_date: datetime
    order_id: UUID
    supplier_id: UUID
    branch_id: UUID
    warehouse_id: UUID
    total: float
    is_posted: bool
    items: list[PurchaseReceiptItemResponse] = []
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
