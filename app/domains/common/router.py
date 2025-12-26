from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.domains.payment.services.payment_service import PaymentService
from app.domains.payment.schemas import PaymentCreate, PaymentResponse, PaymentUpdate

router = APIRouter()


@router.get("/list", response_model=List[PaymentResponse])
def list_payments(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return PaymentService.get_list(db, skip, limit)


@router.post("/create", response_model=PaymentResponse, include_in_schema=False)
def create_payment(data: PaymentCreate, db: Session = Depends(get_db)):
    return PaymentService.create_payment(db, data)