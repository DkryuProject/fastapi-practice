from sqlalchemy.orm import Session
from app.domains.payment.schemas import ManualPaymentRequest, ManualPaymentRequestLog, PaymentCreate, PaymentLogCreate
from app.domains.payment.interfaces.manual_provider import ManualProviderInterface
from app.domains.payment.services.payment_service import PaymentService
from app.domains.user.models import User

import logging
logger = logging.getLogger(__name__)


def mask_card_number(card_number: str) -> dict:
    if not card_number or len(card_number) < 10:
        return {}

    return {
        "card_bin": card_number[:6],
        "last4": card_number[-4:],
        "masked": f"{card_number[:6]}******{card_number[-4:]}",
    }


def mask_phone(phone: str) -> str:
    if len(phone) < 7:
        return "***"
    return phone[:3] + "****" + phone[-4:]


class ManualPaymentService:
    def __init__(self, provider: ManualProviderInterface):
        self.provider = provider

    async def approve(self, db: Session, data: ManualPaymentRequest, user: User):
        payment_number = PaymentService.generate_payment_number()

        payment_payload = PaymentCreate(
            user_id=user.id,
            payment_number=payment_number,
            type="manual",
            amount=data.amount,
            status="request"
        )
    
        payment = PaymentService.create_payment(db, payment_payload)

        PaymentService.update_interface_status(db, payment, "PENDING")

        card_info = mask_card_number(data.card_number)
        request_log = ManualPaymentRequestLog(
            order_number=payment_number,
            amount=data.amount,
            quota=data.quota,
            buyer_name=data.buyer_name,
            goods_name=data.goods_name,
            phone=mask_phone(data.phone),
            card_number=card_info.get("masked"),
            expire=f"{data.expire_year}/**",
        )

        try:
            result = await self.provider.approve(db, payment_number, data)

            PaymentService.update_interface_status(db, payment, "SUCCESS")

        except Exception as e:
            PaymentService.update_interface_status(db, payment, "ERROR")

            PaymentService.write_log(
                db, payment.id,
                PaymentLogCreate(
                    provider="manual",
                    action="approve",
                    request_data=request_log,
                    response_data={"error": str(e)},
                    status="ERROR"
                )
            )
            raise e

        PaymentService.save_manual_detail(db, payment.id, request_log, result)

        PaymentService.write_log(
            db,
            payment.id,
            PaymentLogCreate(
                provider="manual",
                action="approve",
                request_data=request_log,
                response_data=result,
                status="SUCCESS",
            )
        )

        return payment    
