from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db

from app.domains.payment.interfaces.cash_provider import CashReceiptProvider
from app.domains.payment.services.cash_receipt_service import CashReceiptService
from app.domains.payment.schemas import CashBillUserRequest, CashReceiptCreate, PaymentResponse
from app.core.security import get_current_user
from app.domains.user.models import User

router = APIRouter()


async def get_cash_provider() -> CashReceiptProvider:
    return CashReceiptProvider()


@router.get("/check-is-member/{business_number}")
def check_is_member(
        business_number,
        provider: CashReceiptProvider = Depends(get_cash_provider)
):
    service = CashReceiptService(provider)
    result = service.check_is_member(business_number)

    if not result:
        raise HTTPException(status_code=500, detail="check failed")

    return result


@router.get("/company-info/{business_number}")
def get_company_info(
        business_number,
        provider: CashReceiptProvider = Depends(get_cash_provider)
):
    service = CashReceiptService(provider)
    result = service.get_company_info(business_number)

    if not result:
        raise HTTPException(status_code=500, detail="Get company info failed")

    return result


@router.post("/join-member", response_model=PaymentResponse)
def join_member(
        data: CashBillUserRequest,
        db: Session = Depends(get_db),
        provider: CashReceiptProvider = Depends(get_cash_provider),
        current_user: User = Depends(get_current_user)
):
    service = CashReceiptService(provider)
    payment = service.join_member(db, data, current_user)

    if not payment:
        raise HTTPException(status_code=500, detail="issue failed")

    return payment


@router.post("/issue", response_model=PaymentResponse)
def issue_cash_receipt(
    data: CashReceiptCreate, 
    db: Session = Depends(get_db),
    provider: CashReceiptProvider = Depends(get_cash_provider),
    current_user: User = Depends(get_current_user)
):
    service = CashReceiptService(provider)
    payment = service.issue_receipt(db, data, current_user)

    if not payment:
        raise HTTPException(status_code=500, detail="issue failed")
    
    return payment
