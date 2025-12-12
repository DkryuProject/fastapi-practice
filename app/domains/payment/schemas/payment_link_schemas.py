from pydantic import BaseModel


class LinkPaymentCreate(BaseModel):
    order_number: str
    amount: int
    product_name: str


class LinkPaymentResult(BaseModel):
    pay_url: str
    tid: str
    status: str
