from sqlalchemy.orm import Session
from app.domains.payment.schemas import SMSPaymentRequest, PaymentLogCreate
from app.domains.payment.interfaces.sms_provider import SMSProviderInterface
from app.domains.payment.services import PaymentService


class SMSPaymentService:
    def __init__(self, provider: SMSProviderInterface):
        self.provider = provider

    async def request_sms_payment(self, db: Session, data: SMSPaymentRequest):
        order_number = PaymentService.generate_order_number()

        payment_payload = {
            "order_number": order_number,
            "type": "sms",
            "amount": data.amount,
            "phone": data.phone,
            "product_name": data.product_name,
            "order_name": data.order_name,
        }

        payment = PaymentService.create_payment(db, payment_payload)

        PaymentService.update_status(db, payment, "PENDING")

        try:
            result = await self.provider.send_sms(
                phone=data.phone,
                amount=data.amount,
                name=data.order_name,
                product_name=data.product_name
            )

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

        PaymentService.save_sms_detail(db, payment.id, payment_payload, result)

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
