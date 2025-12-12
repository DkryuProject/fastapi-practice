from pydantic import BaseModel


class ManualCardPaymentCreate(BaseModel):
    order_number: str
    amount: int
    card_number: str
    expiry: str
    cvc: str


class ManualCardPaymentResult(BaseModel):
    approval_no: str
    issuer: str
    status: str
    last4: str
