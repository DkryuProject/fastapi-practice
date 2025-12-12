from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

from app.domains.payment.interfaces.cash_receipt_provider import DummyCashReceiptProvider
from app.domains.payment.services.cash_receipt_service import CashReceiptService
from app.domains.payment.schemas import CashReceiptCreate, PaymentResponse

router = APIRouter()

provider = DummyCashReceiptProvider()
service = CashReceiptService(provider)


@router.post("/issue", response_model=PaymentResponse)
def issue_cash_receipt(data: CashReceiptCreate, db: Session = Depends(get_db)):
    return service.issue_receipt(db, data)
