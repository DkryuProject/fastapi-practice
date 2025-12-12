from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

from app.domains.payment.interfaces.cash_receipt_provider import DummyCashReceiptProvider
from app.domains.payment.services.cash_receipt_service import CashReceiptService
from app.domains.payment.schemas.cash_receipt_schemas import CashReceiptCreate
from app.domains.payment.schemas.payment_schemas import PaymentResponse

router = APIRouter(prefix="/payment/cash-receipt", tags=["payment-cash"])

provider = DummyCashReceiptProvider()
service = CashReceiptService(provider)


@router.post("/issue", response_model=PaymentResponse)
def issue_cash_receipt(data: CashReceiptCreate, db: Session = Depends(get_db)):
    return service.issue_receipt(db, data)
