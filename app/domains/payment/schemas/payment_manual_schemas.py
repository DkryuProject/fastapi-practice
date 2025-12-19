from pydantic import BaseModel
from typing import Optional


class ManualPaymentRequest(BaseModel):
    amount: int
    card_number: str
    expire_year: str
    expire_month: str
    quota: str
    buyer_name: str
    goods_name: str
    phone: str


class ManualPaymentRequestLog(BaseModel):
    order_number: str
    amount: int
    card_number: str
    expire: str
    quota: str
    buyer_name: str
    goods_name: str
    phone: str


class ManualPaymentResult(BaseModel):
    tid: Optional[str] = None
    code: Optional[str] = None
    message: Optional[str] = None
    app_number: Optional[str] = None
    app_date: Optional[str] = None
    van_cp_cd: Optional[str] = None
    cp_cd: Optional[str] = None
    van_iss_cp_cd: Optional[str] = None
    iss_cp_cd: Optional[str] = None
