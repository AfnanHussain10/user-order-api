from typing import Optional
from pydantic import BaseModel, Field, condecimal
from datetime import datetime


# Shared properties
class OrderBase(BaseModel):
    total_amount: condecimal(ge=0, decimal_places=2) = Field(..., description="Total amount of the order")
    status: Optional[str] = "pending"


# Properties to receive on order creation
class OrderCreate(OrderBase):
    pass


# Properties to receive on order update
class OrderUpdate(BaseModel):
    total_amount: Optional[condecimal(ge=0, decimal_places=2)] = None
    status: Optional[str] = None


# Properties to return to client
class OrderResponse(OrderBase):
    id: int
    user_id: int
    order_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True