from sqlalchemy.orm import Session
from app.domains.payment.schemas import (
    PaymentCreate, PaymentLogCreate, CashBillUserRequest, CashBillUserCreate, CashReceiptCreate
)
from app.domains.payment.interfaces.cash_receipt_provider import CashReceiptProviderInterface
from app.domains.payment.services import PaymentService
from app.domains.user.models import User
from app.domains.payment.crud import PaymentCRUD
import logging
logger = logging.getLogger(__name__)


def create_cashbill_user(db: Session, user_id: int, data: CashBillUserRequest):
    return PaymentCRUD.save_cashbill_user(db, user_id, data)


class CashReceiptService:
    def __init__(self, provider: CashReceiptProviderInterface):
        self.provider = provider

    def check_is_member(self, business_number):

        result = self.provider.check_member(business_number)

        return result

    def get_company_info(self, business_number):

        result = self.provider.company_info(business_number)

        return result

    def join_member(self, db: Session, data: CashBillUserRequest, user: User):
        try:
            result = self.provider.join_member(data)
            logger.exception("팝빌 회원 가입 결과: %s", result)

            if result.code == 1:
                user = create_cashbill_user(db, user.id, data)

            db.commit()
            db.refresh(user)

        except Exception as e:
            db.rollback()
            logger.exception("팝빌 회원 가입 실패: %s", e)
            raise e

        return result

    def issue_receipt(self, db: Session, data: CashReceiptCreate, user: User):
        
        order_number = PaymentService.generate_order_number()

        payment_payload = PaymentCreate(
            user_id=user.id,
            order_number=order_number,
            type="cash",
            amount=data.amount,
        )

        payment = PaymentService.create_payment(db, payment_payload)

        result = self.provider.issue(data.amount, data.receipt_type, data.identity)

        PaymentService.write_log(
            db,
            payment.id,
            PaymentLogCreate(
                provider="cash_receipt",
                action="issue",
                request_data=data.dict(),
                response_data=result,
                status=result.get("status"),
            ),
        )

        PaymentService.save_cash_receipt_detail(db, payment.id, result)

        return payment
