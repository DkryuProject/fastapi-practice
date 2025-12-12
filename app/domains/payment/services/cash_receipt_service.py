from sqlalchemy.orm import Session
from app.domains.payment.schemas.cash_receipt_schemas import CashReceiptCreate
from app.domains.payment.schemas.payment_schemas import PaymentCreate, PaymentLogCreate
from app.domains.payment.interfaces.cash_receipt_provider import CashReceiptProviderInterface
from app.domains.payment.services.payment_service import PaymentService


class CashReceiptService:
    def __init__(self, provider: CashReceiptProviderInterface):
        self.provider = provider

    def issue_receipt(self, db: Session, data: CashReceiptCreate):
        payment_payload = PaymentCreate(
            order_number=data.order_number,
            type="cash_receipt",
            amount=data.amount,
            status="issued",
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
