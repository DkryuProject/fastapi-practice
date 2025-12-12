from sqlalchemy.orm import Session
from app.domains.payment.models import (
    Payment,
    PaymentLog,
    PaymentSMS,
    PaymentLink,
    PaymentManualCard,
    PaymentCashReceipt,
)
from app.domains.payment.schemas.payment_schemas import PaymentCreate, PaymentUpdate, PaymentLogCreate
from typing import Optional


class PaymentCRUD:
    @staticmethod
    def create_payment(db: Session, data: PaymentCreate) -> Payment:
        obj = Payment(**data.dict())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def get_payment(db: Session, payment_id: int) -> Optional[Payment]:
        return db.query(Payment).filter(Payment.id == payment_id).first()

    @staticmethod
    def get_by_order_number(db: Session, order_number: str) -> Optional[Payment]:
        return db.query(Payment).filter(Payment.order_number == order_number).first()

    @staticmethod
    def get_list(db: Session, skip=0, limit=50):
        return (
            db.query(Payment)
            .order_by(Payment.id.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def update_payment(db: Session, db_obj: Payment, data: PaymentUpdate) -> Payment:
        for field, value in data.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def delete_payment(db: Session, payment_id: int) -> Optional[Payment]:
        obj = db.query(Payment).filter(Payment.id == payment_id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    @staticmethod
    def create_log(db: Session, payment_id: int, data: PaymentLogCreate) -> PaymentLog:
        obj = PaymentLog(payment_id=payment_id, **data.dict())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    # ----- detail save helpers -----
    @staticmethod
    def save_sms_detail(db: Session, payment_id: int, payload: dict) -> PaymentSMS:
        obj = PaymentSMS(
            payment_id=payment_id,
            sms_provider=payload.get("provider") or payload.get("sms_provider"),
            sms_transaction_id=payload.get("sms_tid") or payload.get("transaction_id"),
            send_status=payload.get("status") or payload.get("send_status"),
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def save_link_detail(db: Session, payment_id: int, payload: dict) -> PaymentLink:
        obj = PaymentLink(
            payment_id=payment_id,
            pg_tid=payload.get("tid") or payload.get("pg_tid"),
            pay_url=payload.get("pay_url"),
            expire_at=payload.get("expire_at"),
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def save_manual_card_detail(db: Session, payment_id: int, payload: dict) -> PaymentManualCard:
        obj = PaymentManualCard(
            payment_id=payment_id,
            card_bin=payload.get("card_bin"),
            card_last4=payload.get("last4") or payload.get("card_last4"),
            approval_no=payload.get("approval_no"),
            issuer=payload.get("issuer"),
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def save_cash_receipt_detail(db: Session, payment_id: int, payload: dict) -> PaymentCashReceipt:
        obj = PaymentCashReceipt(
            payment_id=payment_id,
            receipt_no=payload.get("receipt_no"),
            receipt_type=payload.get("receipt_type"),
            approval_no=payload.get("approval_no"),
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
