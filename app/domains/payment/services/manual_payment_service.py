from sqlalchemy.orm import Session
from app.domains.payment.schemas.payment_manual_schemas import ManualCardPaymentCreate
from app.domains.payment.schemas.payment_schemas import PaymentCreate, PaymentLogCreate
from app.domains.payment.interfaces.manual_provider import ManualCardProviderInterface
from app.domains.payment.services.payment_service import PaymentService


class ManualCardPaymentService:
    def __init__(self, provider: ManualCardProviderInterface):
        self.provider = provider

    def approve_card(self, db: Session, data: ManualCardPaymentCreate):
        payment_payload = PaymentCreate(
            order_number=data.order_number,
            type="manual_card",
            amount=data.amount,
            status="processing",
        )
        payment = PaymentService.create_payment(db, payment_payload)

        # 실제로는 카드번호 등 민감정보 취급 유의 (로그에선 마스킹)
        result = self.provider.approve(data.card_number, data.expiry, data.cvc, data.amount)

        PaymentService.write_log(
            db,
            payment.id,
            PaymentLogCreate(
                provider="manual_card",
                action="approve",
                request_data={"card_bin": data.card_number[:6], "last4": data.card_number[-4:], "expiry": data.expiry},
                response_data=result,
                status=result.get("status"),
            ),
        )

        PaymentService.save_manual_card_detail(db, payment.id, result)

        # 상태 업데이트 예: approved -> success
        # (여기서는 단순히 status를 success로 바꿈)
        from app.domains.payment.schemas.payment_schemas import PaymentUpdate
        PaymentService.update_payment(db, payment.id, PaymentUpdate(status="success"))

        return payment
