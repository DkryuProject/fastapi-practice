from pydantic import BaseModel
from typing import Optional


class SMSPaymentCreate(BaseModel):
    order_number: str
    phone: str
    message: str
    amount: int


class SMSPaymentResult(BaseModel):
    sms_tid: str
    send_status: str
    raw: Optional[dict] = None
