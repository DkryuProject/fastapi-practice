from sqlalchemy.orm import Session
from app.domains.payment.schemas import PaymentCreate, PaymentLogCreate, CashReceiptCreate
from app.domains.payment.interfaces.cash_receipt_provider import CashReceiptProviderInterface
from app.domains.payment.services.payment_service import PaymentService
from app.domains.user.models import User


class CashReceiptService:
    def __init__(self, provider: CashReceiptProviderInterface):
        self.provider = provider

    async def issue_receipt(self, db: Session, data: CashReceiptCreate, user: User):
        
        order_number = PaymentService.generate_order_number()

        payment_payload = PaymentCreate(
            user_id=user.id,
            order_number=order_number,
            type="cash",
            amount=data.amount,
        )

        payment = PaymentService.create_payment(db, payment_payload)

        result = await self.provider.issue(data.amount, data.receipt_type, data.identity)

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
