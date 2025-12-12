from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

from app.domains.payment.interfaces.pg_provider import DummyPGProvider
from app.domains.payment.services.link_payment_service import LinkPaymentService
from app.domains.payment.schemas import LinkPaymentCreate

router = APIRouter()

pg = DummyPGProvider()
service = LinkPaymentService(pg)


@router.post("/request")
def create_link_payment(data: LinkPaymentCreate, db: Session = Depends(get_db)):
    return service.create_link_payment(db, data)
