from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.core.database import get_db
from app.domains.payment.services.payment_service import PaymentService
from app.domains.payment.schemas import PaymentCreate, PaymentResponse, PaymentUpdate
from app.domains.common.schemas import Page


PaymentPageResponse = Page[PaymentResponse]


router = APIRouter()


@router.get("/list", response_model=PaymentPageResponse, summary="결재 리스트 조회")
def list_payments(    
    page: int = 1,
    size: int = 50, 
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * size

    items, total = PaymentService.get_list(
        db=db,
        skip=skip,
        limit=size,
        current_user=current_user,
    )

    return {
        "items": items,
        "page": page,
        "size": size,
        "total": total,
        "has_next": page * size < total,
    }

@router.post("/create", response_model=PaymentResponse, summary="결제 생성", include_in_schema=False)
def create_payment(data: PaymentCreate, db: Session = Depends(get_db)):
    return PaymentService.create_payment(db, data)


@router.get("/{payment_id}", response_model=PaymentResponse, summary="결제 상세 조회")
def get_payment(
    payment_id: int, 
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    obj = PaymentService.get_payment(db, payment_id, current_user)

    if not obj:
        raise HTTPException(status_code=404, detail="payment not found")
    
    return obj


@router.patch("/{payment_id}", response_model=PaymentResponse, summary="결제 수정")
def update_payment(
    payment_id: int, 
    data: PaymentUpdate, 
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    obj = PaymentService.update_payment(db, payment_id, data, current_user)

    if not obj:
        raise HTTPException(status_code=404, detail="payment not found")
    
    return obj


@router.delete("/{payment_id}", summary="결제 삭제")
def delete_payment(
    payment_id: int, 
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    PaymentService.delete_payment(db, payment_id, current_user)
    return {"message": "deleted"}
