from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class PaymentBase(BaseModel):
    order_number: str
    type: str
    amount: int
    status: str
    customer_name: Optional[str] = None
    phone: Optional[str] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    status: Optional[str] = None
    amount: Optional[int] = None


class PaymentResponse(PaymentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PaymentLogCreate(BaseModel):
    provider: str
    action: str
    request_data: Optional[Any] = None
    response_data: Optional[Any] = None
    status: Optional[str] = None


class PaymentLogResponse(BaseModel):
    id: int
    provider: str
    action: str
    request_data: Any
    response_data: Any
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
