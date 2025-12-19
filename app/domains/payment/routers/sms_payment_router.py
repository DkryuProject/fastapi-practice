from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db

from app.domains.payment.interfaces.sms_provider import SMSProvider
from app.domains.payment.services.sms_payment_service import SMSPaymentService
from app.domains.payment.schemas import SMSPaymentRequest, PaymentResponse
from app.core.security import get_current_user
from app.domains.user.models import User

router = APIRouter()


async def get_sms_provider() -> SMSProvider:
    return SMSProvider() 


@router.post("/request", response_model=PaymentResponse)
async def request_sms_payment(
    data: SMSPaymentRequest,
    db: Session = Depends(get_db),
    provider: SMSProvider = Depends(get_sms_provider),
    current_user: User = Depends(get_current_user)
):
    service = SMSPaymentService(provider)
    payment = await service.request_sms_payment(db, data, current_user)
    if not payment:
        raise HTTPException(status_code=500, detail="sms payment failed")
    return payment
