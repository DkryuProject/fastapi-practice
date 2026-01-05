from pydantic import BaseModel


class LinkPaymentCreateRequest(BaseModel):
    amount: int
    product_name: str
    purchase_name: str
    phone: str
    payment_type: str
    pay_method: str


class LinkPaymentCancelRequest(BaseModel):
    id: int
    cancel_reason: str


class LinkPaymentResult(BaseModel):
    pay_url: str
    tid: str
    status: str
