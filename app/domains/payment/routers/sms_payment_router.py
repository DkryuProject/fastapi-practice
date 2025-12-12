from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db

from app.domains.payment.interfaces.sms_provider import SMSProvider
from app.domains.payment.services.sms_payment_service import SMSPaymentService
from app.domains.payment.schemas import SMSPaymentRequest, PaymentResponse

router = APIRouter()


async def get_sms_provider() -> SMSProvider:
    return SMSProvider() 


@router.post("/request", response_model=PaymentResponse)
async def request_sms_payment(
    data: SMSPaymentRequest,
    db: Session = Depends(get_db),
    provider: SMSProvider = Depends(get_sms_provider)
):
    service = SMSPaymentService(provider)
    payment = await service.request_sms_payment(db, data)
    if not payment:
        raise HTTPException(status_code=500, detail="sms payment failed")
    return payment
