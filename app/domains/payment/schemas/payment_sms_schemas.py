from pydantic import BaseModel
from typing import Optional


class SMSPaymentRequest(BaseModel):
    phone: str
    amount: int
    product_name: str
    order_name: str


class SMSPaymentResult(BaseModel):
    sms_tid: str
    send_status: str
    raw: Optional[dict] = None
