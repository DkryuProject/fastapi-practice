from pydantic import BaseModel
from typing import Optional


class SMSPaymentRequest(BaseModel):
    phone: str
    amount: int
    product_name: str
    order_name: str


class SMSPaymentResult(BaseModel):
    rid: str
    code: str
    message: str
    request_date: str
    send_status: str
