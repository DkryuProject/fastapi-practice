from sqlalchemy.orm import Session
from app.domains.payment.schemas import SMSPaymentRequest, PaymentLogCreate, PaymentCreate
from app.domains.payment.interfaces.sms_provider import SMSProviderInterface
from app.domains.payment.services import PaymentService


class SMSPaymentService:
    def __init__(self, provider: SMSProviderInterface):
        self.provider = provider

    async def request_sms_payment(self, db: Session, data: SMSPaymentRequest):
        order_number = PaymentService.generate_order_number()

        payment_payload = PaymentCreate(
            order_number=order_number,
            type="sms",
            amount=data.amount,
        )
        payment = PaymentService.create_payment(db, payment_payload)

        PaymentService.update_status(db, payment, "PENDING")

        try:
            result = await self.provider.send_sms(data)

            PaymentService.update_status(db, payment, "SUCCESS")

        except Exception as e:
            PaymentService.update_status(db, payment, "ERROR")

            PaymentService.write_log(
                db, payment.id,
                PaymentLogCreate(
                    provider="sms",
                    action="send",
                    request_data=data.dict(),
                    response_data={"error": str(e)},
                    status="ERROR"
                )
            )
            raise e

        PaymentService.save_sms_detail(db, payment.id, data, result)

        PaymentService.write_log(
            db,
            payment.id,
            PaymentLogCreate(
                provider="sms",
                action="send",
                request_data=data.dict(),
                response_data=result,
                status="SUCCESS",
            )
        )

        return payment
