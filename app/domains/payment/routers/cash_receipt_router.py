from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db

from app.domains.payment.interfaces.cash_receipt_provider import CashReceiptProvider
from app.domains.payment.services.cash_receipt_service import CashReceiptService
from app.domains.payment.schemas import CashReceiptCreate, PaymentResponse
from app.core.security import get_current_user
from app.domains.user.models import User

router = APIRouter()


async def get_cash_provider() -> CashReceiptProvider:
    return CashReceiptProvider() 


@router.post("/issue", response_model=PaymentResponse)
async def issue_cash_receipt(
    data: CashReceiptCreate, 
    db: Session = Depends(get_db),
    provider: CashReceiptProvider = Depends(get_cash_provider),
    current_user: User = Depends(get_current_user)
):
    service = CashReceiptService(provider)
    payment = await service.issue_receipt(db, data, current_user)

    if not payment:
        raise HTTPException(status_code=500, detail="issue failed")
    
    return payment
