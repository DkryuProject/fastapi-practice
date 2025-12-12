from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db

from app.domains.payment.interfaces.sms_provider import DummySMSProvider
from app.domains.payment.services.sms_payment_service import SMSPaymentService
from app.domains.payment.schemas import SMSPaymentCreate, PaymentResponse

router = APIRouter()

provider = DummySMSProvider()
service = SMSPaymentService(provider)


@router.post("/request", response_model=PaymentResponse)
def request_sms_payment(data: SMSPaymentCreate, db: Session = Depends(get_db)):
    payment = service.request_sms_payment(db, data)
    if not payment:
        raise HTTPException(status_code=500, detail="sms payment failed")
    return payment
