from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db

from app.domains.payment.interfaces.sms_provider import DummySMSProvider
from app.domains.payment.services.sms_payment_service import SMSPaymentService
from app.domains.payment.schemas.payment_sms_schemas import SMSPaymentCreate
from app.domains.payment.schemas.payment_schemas import PaymentResponse

router = APIRouter(prefix="/payment/sms", tags=["payment-sms"])

provider = DummySMSProvider()
service = SMSPaymentService(provider)


@router.post("/", response_model=PaymentResponse)
def request_sms_payment(data: SMSPaymentCreate, db: Session = Depends(get_db)):
    payment = service.request_sms_payment(db, data)
    if not payment:
        raise HTTPException(status_code=500, detail="sms payment failed")
    return payment
