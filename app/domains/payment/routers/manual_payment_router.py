from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db

from app.domains.payment.interfaces.manual_provider import ManualProvider
from app.domains.payment.services.manual_payment_service import ManualPaymentService
from app.domains.payment.schemas import ManualPaymentRequest, PaymentResponse
from app.core.security import get_current_user
from app.domains.user.models import User

router = APIRouter()


async def get_manual_provider() -> ManualProvider:
    return ManualProvider()


@router.post("/approve", response_model=PaymentResponse, summary="수기 결제")
async def approve(
        data: ManualPaymentRequest,
        db: Session = Depends(get_db),
        provider: ManualProvider = Depends(get_manual_provider),
        current_user: User = Depends(get_current_user)
):
    service = ManualPaymentService(provider)
    payment = await service.approve(db, data, current_user)

    if not payment:
        raise HTTPException(status_code=500, detail="approval failed")
    return payment


@router.post("/cancel", response_model=PaymentResponse, summary="수기 결제 취소")
async def approve(
        data: ManualPaymentRequest,
        db: Session = Depends(get_db),
        provider: ManualProvider = Depends(get_manual_provider),
        current_user: User = Depends(get_current_user)
):
    service = ManualPaymentService(provider)
    payment = await service.approve(db, data, current_user)

    if not payment:
        raise HTTPException(status_code=500, detail="approval failed")
    return payment
