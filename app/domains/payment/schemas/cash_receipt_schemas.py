from pydantic import BaseModel


class CashReceiptCreate(BaseModel):
    order_number: str
    amount: int
    receipt_type: str   # 소득공제 / 지출증빙
    identity: str       # 휴대폰 / 사업자번호


class CashReceiptResult(BaseModel):
    receipt_no: str
    approval_no: str
    status: str
