from sqlalchemy.orm import Session
from app.domains.payment.schemas.payment_link_schemas import LinkPaymentCreate
from app.domains.payment.schemas.payment_schemas import PaymentCreate, PaymentLogCreate
from app.domains.payment.interfaces.pg_provider import PGProviderInterface
from app.domains.payment.services.payment_service import PaymentService


class LinkPaymentService:
    def __init__(self, pg_provider: PGProviderInterface):
        self.pg = pg_provider

    def create_link_payment(self, db: Session, data: LinkPaymentCreate):
        payment_payload = PaymentCreate(
            order_number=data.order_number,
            type="link",
            amount=data.amount,
            status="ready",
        )
        payment = PaymentService.create_payment(db, payment_payload)

        result = self.pg.create_payment_link(data.amount, data.product_name, data.order_number)

        PaymentService.write_log(
            db,
            payment.id,
            PaymentLogCreate(
                provider="pg",
                action="create_link",
                request_data=data.dict(),
                response_data=result,
                status=result.get("status"),
            ),
        )

        PaymentService.save_link_detail(db, payment.id, result)

        return {"payment_id": payment.id, "pay_url": result.get("pay_url")}
