from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

from app.domains.payment.interfaces.pg_provider import DummyPGProvider
from app.domains.payment.services.link_payment_service import LinkPaymentService
from app.domains.payment.schemas.payment_link_schemas import LinkPaymentCreate

router = APIRouter(prefix="/payment/link", tags=["payment-link"])

pg = DummyPGProvider()
service = LinkPaymentService(pg)


@router.post("/")
def create_link_payment(data: LinkPaymentCreate, db: Session = Depends(get_db)):
    return service.create_link_payment(db, data)
