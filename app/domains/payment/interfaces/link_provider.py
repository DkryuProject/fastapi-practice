import httpx

from sqlalchemy.orm import Session
from abc import ABC, abstractmethod
from app.utils.retry import retry_request
from app.domains.payment.models import Payment
from app.domains.view.schemas import LinkPaymentViewRequest
from app.core.config import settings
from app.domains.payment.services.payment_service import PaymentService


class LinkProviderInterface(ABC):
    @abstractmethod
    async def cancel(self, db: Session, payload) -> dict:
        raise NotImplementedError()


class LinkProvider(LinkProviderInterface):
    async def cancel(self, db: Session, payload) -> dict:
        async def http_call():
            async with httpx.AsyncClient(timeout=3) as client:
                resp = await client.post(
                    "https://pgapi.korpay.com/cancelTransJson.do",
                    json=payload,
                )
                resp.raise_for_status()
                return resp.json()

        body = await retry_request(http_call)

        if body.get("resCd") != "0000":
            raise ValueError(body.get("resMsg"))

        # 3. 취소 결과 저장
        #PaymentCRUD.create_payment_cancel(db, body)

        return {
            "message": "취소 성공",
            "cancel_date": body.get("CancelDate"),
            "cancel_time": body.get("CancelTime"),
            "tid": body.get("tid"),
        }
