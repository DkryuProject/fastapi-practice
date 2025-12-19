from pydantic import BaseModel


class CashReceiptCreate(BaseModel):
    amount: int
    identity: str       # 휴대폰 / 사업자번호


class CashReceiptResult(BaseModel):
    receipt_no: str
    approval_no: str
    status: str
