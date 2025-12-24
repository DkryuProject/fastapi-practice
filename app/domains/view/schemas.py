from pydantic import BaseModel


class PaymentViewSchema(BaseModel):
    payment_id: int
    order_number: str
    amount: int

    product_name: str
    purchase_name: str | None
    phone: str | None

    token: str

    class Config:
        from_attributes = True


class LinkPaymentViewRequest(BaseModel):
    product_name: str
    amount: int
    card_code: str
    installment: str
    shop_transaction_id: str
