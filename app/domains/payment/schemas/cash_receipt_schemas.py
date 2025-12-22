from pydantic import BaseModel


class CashBillUserRequest(BaseModel):
    ID: str
    Password: str
    LinkID: str
    CorpNum: str
    CEOName: str
    CorpName: str
    Addr: str
    BizType: str
    BizClass: str
    ContractName: str
    ContractEmail: str
    ContractTEL: str


class CashBillUserCreate(BaseModel):
    user_id: int
    pobbill_user_id: str
    password: str


class CashReceiptCreate(BaseModel):
    amount: int
    identity: str


class CashReceiptResult(BaseModel):
    receipt_no: str
    approval_no: str
    status: str
