import httpx
import hashlib
from app.core.config import settings
from abc import ABC, abstractmethod
from app.utils.retry import retry_request
from datetime import datetime, time
from app.domains.payment.schemas import SMSPaymentRequest, SMSPaymentResult


def get_default_limit_date() -> str:
    now = datetime.now()
    limit_datetime = datetime.combine(now.date(), time(hour=23, minute=0, second=0))
    return limit_datetime.strftime("%Y%m%d%H%M%S")


class SMSProviderInterface(ABC):
    @abstractmethod
    async def send_sms(self, data: SMSPaymentRequest) -> SMSPaymentResult:
        raise NotImplementedError()


def make_hash(mid: str, amount: int, mkey: str) -> str:
    plain_text = f"{mid}{amount}{mkey}"
    return hashlib.sha256(plain_text.encode()).hexdigest()


class SMSProvider(SMSProviderInterface):
    BASE_URL = settings.sms_api_url

    async def send_sms(self, data: SMSPaymentRequest) -> SMSPaymentResult:
        limit_date = get_default_limit_date()
        payload = {
            "mid": settings.mid,
            "amount": data.amount,
            "orderHp": data.phone,
            "orderName": data.order_name,
            "productName": data.product_name,
            "limitDate": limit_date,
            "hash": make_hash(settings.mid, data.amount, settings.mkey),
            "mkey": settings.mkey
        }

        async def http_call():
            async with httpx.AsyncClient(timeout=3) as client:
                resp = await client.post(
                    self.BASE_URL,
                    json=payload
                )
                resp.raise_for_status()
                return resp.json()

        raw = await retry_request(http_call)

        return SMSPaymentResult(
            rid=raw.get("RID"),
            code=raw.get("resultCode"),
            message=raw.get("resultMessage"),
            request_date=raw.get("requestDate"),
            send_status=raw.get("status"),
        )


class DummySMSProvider(SMSProviderInterface):
    async def send_sms(self, data: SMSPaymentRequest) -> dict:
        return {
            "sms_tid": "SMS" + data.phone[-4:],
            "status": "sent",
            "provider": "dummy_sms",
            "raw": {"phone": data.phone, "message": data.message},
        }
