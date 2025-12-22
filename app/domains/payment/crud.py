from sqlalchemy.orm import Session
from app.domains.payment.models import (
    Payment,
    PaymentLog,
    PaymentSMS,
    PaymentLinkRequest,
    PaymentManual,
    PaymentCashReceipt,
    CashBillUser
)
from app.domains.payment.schemas import (
    PaymentUpdate, 
    PaymentLogCreate, 
    SMSPaymentResult, 
    SMSPaymentRequest,
    ManualPaymentRequestLog,
    ManualPaymentResult,
    CashBillUserRequest
)
from typing import Optional


class PaymentCRUD:
    @staticmethod
    def create_payment(db: Session, data) -> Payment:
        obj = Payment(**data.model_dump())
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
    def save_sms_detail(db: Session, payment_id: int, payload: SMSPaymentRequest, result: SMSPaymentResult) -> PaymentSMS:
        obj = PaymentSMS(
            payment_id=payment_id,
            product_name=payload.product_name,
            order_name=payload.order_name,
            amount=payload.amount,
            phone=payload.phone,

            rid=result.rid,
            code=result.code,
            message=result.message,
            request_date=result.request_date,
            send_status=result.send_status,
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def save_link_detail(db: Session, payment_id: int, payload: dict) -> PaymentLinkRequest:
        obj = PaymentLinkRequest(
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
    def save_manual_detail(db: Session, payment_id: int, request: ManualPaymentRequestLog, result: ManualPaymentResult) -> PaymentManual:
        obj = PaymentManual(
            payment_id=payment_id,
            amount = request.amount,
            card_number = request.card_number,
            expire = request.expire,
            quota = request.quota,
            buyer_name = request.buyer_name,
            goods_name = request.goods_name,
            phone = request.phone,

            tid = result.tid,
            code = result.code,
            message = result.message,
            app_number = result.app_number,
            app_date = result.app_date,
            van_cp_cd = result.van_cp_cd,
            cp_cd = result.cp_cd,
            van_iss_cp_cd = result.van_cp_cd,
            iss_cp_cd = result.iss_cp_cd,
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

    @staticmethod
    def save_cashbill_user(db: Session, user_id: int, payload: CashBillUserRequest) -> CashBillUser:
        obj = CashBillUser(
            user_id=user_id,
            pobbill_user_id=payload.ID,
            password=payload.Password,
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
