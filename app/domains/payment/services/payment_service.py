from sqlalchemy.orm import Session
from app.domains.payment.crud import PaymentCRUD
from app.domains.payment.schemas.payment_schemas import PaymentCreate, PaymentUpdate, PaymentLogCreate
from app.domains.payment.services.state_machine import PaymentStateMachine
from datetime import datetime


class PaymentService:
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
    def save_sms_detail(db: Session, payment_id: int, payload: dict, result: dict):
        return PaymentCRUD.save_sms_detail(db, payment_id, payload, result)

    @staticmethod
    def save_link_detail(db: Session, payment_id: int, payload: dict):
        return PaymentCRUD.save_link_detail(db, payment_id, payload)

    @staticmethod
    def save_manual_card_detail(db: Session, payment_id: int, payload: dict):
        return PaymentCRUD.save_manual_card_detail(db, payment_id, payload)

    @staticmethod
    def save_cash_receipt_detail(db: Session, payment_id: int, payload: dict):
        return PaymentCRUD.save_cash_receipt_detail(db, payment_id, payload)

    @staticmethod
    def update_status(db, payment, new_status: str):
        PaymentStateMachine.assert_transition(payment.status, new_status)

        payment.status = new_status
        db.commit()
        db.refresh(payment)

        return payment
    
    @staticmethod
    def generate_order_number(prefix: str = "aisystem", seq: int = 1) -> str:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{prefix}_{timestamp}_{seq:03d}"
