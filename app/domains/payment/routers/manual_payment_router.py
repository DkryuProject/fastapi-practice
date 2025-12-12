from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db

from app.domains.payment.interfaces.manual_provider import DummyManualProvider
from app.domains.payment.services.manual_payment_service import ManualCardPaymentService
from app.domains.payment.schemas.payment_manual_schemas import ManualCardPaymentCreate
from app.domains.payment.schemas.payment_schemas import PaymentResponse

router = APIRouter(prefix="/payment/manual", tags=["payment-manual"])

provider = DummyManualProvider()
service = ManualCardPaymentService(provider)


@router.post("/approve", response_model=PaymentResponse)
def approve_card_payment(data: ManualCardPaymentCreate, db: Session = Depends(get_db)):
    payment = service.approve_card(db, data)
    if not payment:
        raise HTTPException(status_code=500, detail="approval failed")
    return payment
