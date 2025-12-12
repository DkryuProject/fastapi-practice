from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.domains.payment.services.payment_service import PaymentService
from app.domains.payment.schemas.payment_schemas import PaymentCreate, PaymentResponse, PaymentUpdate

router = APIRouter(prefix="/payment", tags=["payment"])


@router.post("/", response_model=PaymentResponse)
def create_payment(data: PaymentCreate, db: Session = Depends(get_db)):
    return PaymentService.create_payment(db, data)


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    obj = PaymentService.get_payment(db, payment_id)
    if not obj:
        raise HTTPException(status_code=404, detail="payment not found")
    return obj


@router.get("/", response_model=List[PaymentResponse])
def list_payments(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return PaymentService.get_list(db, skip, limit)


@router.patch("/{payment_id}", response_model=PaymentResponse)
def update_payment(payment_id: int, data: PaymentUpdate, db: Session = Depends(get_db)):
    obj = PaymentService.update_payment(db, payment_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="payment not found")
    return obj


@router.delete("/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    PaymentService.delete_payment(db, payment_id)
    return {"msg": "deleted"}
