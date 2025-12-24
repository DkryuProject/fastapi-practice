import uuid
import secrets

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.domains.payment.crud import PaymentCRUD
from app.domains.payment.models import PaymentLinkCreate
from app.domains.payment.schemas import (
    PaymentCreate, 
    PaymentUpdate,
    PaymentLogCreate, 
    SMSPaymentRequest, 
    SMSPaymentResult,
    ManualPaymentRequestLog,
    ManualPaymentResult,
    LinkPaymentCreateRequest,
    CashBillUserRequest,
)
from app.domains.view.schemas import PaymentViewSchema
from app.domains.payment.services.state_machine import PaymentStateMachine
from datetime import datetime
import logging
logger = logging.getLogger(__name__)


class PaymentService:
    @staticmethod
    def generate_order_number(prefix: str = "aisystem") -> str:
        return f"{prefix}_{uuid.uuid4().hex[:12]}"

    @staticmethod
    def generate_access_token():
        return secrets.token_urlsafe(32)

    @staticmethod
    def create_payment(db: Session, payload: PaymentCreate):
        return PaymentCRUD.create_payment(db, payload)

    @staticmethod
    def get_payment(db: Session, payment_id: int):
        return PaymentCRUD.get_payment(db, payment_id)

    @staticmethod
    def get_list(db: Session, skip=0, limit=50):
        return PaymentCRUD.get_list(db, skip, limit)

    @staticmethod
    def update_payment(db: Session, payment_id: int, payload: PaymentUpdate):
        db_obj = PaymentCRUD.get_payment(db, payment_id)
        if not db_obj:
            return None
        return PaymentCRUD.update_payment(db, db_obj, payload)

    @staticmethod
    def delete_payment(db: Session, payment_id: int):
        return PaymentCRUD.delete_payment(db, payment_id)

    @staticmethod
    def write_log(db: Session, payment_id: int, log: PaymentLogCreate):
        return PaymentCRUD.create_log(db, payment_id, log)

    @staticmethod
    def save_sms_detail(db: Session, payment_id: int, payload: SMSPaymentRequest, result: SMSPaymentResult):
        return PaymentCRUD.save_sms_detail(db, payment_id, payload, result)

    @staticmethod
    def save_link_create(db: Session, payment_id, data: LinkPaymentCreateRequest):
        token = PaymentService.generate_access_token()
        url = f"http://localhost:8000/request-view/{payment_id}"
        return PaymentCRUD.save_link_create(db, payment_id, url, token, data)

    @staticmethod
    def save_manual_detail(db: Session, payment_id: int, request: ManualPaymentRequestLog, result: ManualPaymentResult):
        return PaymentCRUD.save_manual_detail(db, payment_id, request, result)

    @staticmethod
    def create_cash_receipt_user(db: Session, user_id: int, data: CashBillUserRequest):
        return PaymentCRUD.save_cashbill_user(db, user_id, data)

    @staticmethod
    def save_cash_receipt_detail(db: Session, payment_id: int, payload: dict):
        return PaymentCRUD.save_cash_receipt_detail(db, payment_id, payload)

    @staticmethod
    def update_status(db, payment, new_status: str):
        PaymentStateMachine.assert_transition(payment.interface_status, new_status)

        payment.interface_status = new_status        
        db.commit()
        db.refresh(payment)

        return payment

    @staticmethod
    def create_link_payment(db: Session, data: LinkPaymentCreateRequest, user) -> dict:
        try:
            order_number = PaymentService.generate_order_number()

            payment_payload = PaymentCreate(
                user_id=user.id,
                order_number=order_number,
                type="link",
                amount=data.amount,
                interface_status="SUCCESS",
                status="create",
            )

            payment = PaymentService.create_payment(db, payment_payload)

            result = PaymentService.save_link_create(db, payment.id, data)

            db.commit()

            return {
                "payment_id": payment.id,
                "url": result.url
            }

        except Exception:
            db.rollback()
            logger.exception("링크결제 요청 실패")
            raise

    @staticmethod
    def request_link_payment(db: Session, payment_id: int, data: dict, cert_page_url: str):
        try:
            result = PaymentCRUD.save_link_request(db, payment_id, data, cert_page_url)

            return result

        except Exception:
            logger.exception("링크 결제 요청 저장 실패")
            raise

    @staticmethod
    def result_link_payment(db: Session, body: dict):
        try:
            result = PaymentCRUD.save_link_result(db, payment_id, body)

            return result

        except Exception:
            logger.exception("링크 결제 요청 저장 실패")
            raise

    @staticmethod
    def get_payment_view_by_token(db: Session, token: str) -> PaymentViewSchema:
        link = PaymentCRUD.get_payment_by_link_token(db, token)

        if not link:
            raise HTTPException(status_code=404, detail="잘못된 결제 링크")

        payment = link.payment

        if not payment:
            raise HTTPException(status_code=404, detail="결제 정보 없음")

        return PaymentViewSchema(
            payment_id=payment.id,
            order_number=payment.order_number,
            amount=payment.amount,
            product_name=link.product_name,
            purchase_name=link.purchase_name,
            phone=link.phone,
            token=link.token,
        )