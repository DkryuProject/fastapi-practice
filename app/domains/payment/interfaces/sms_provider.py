import httpx
import hashlib
from app.core.config import settings
from abc import ABC, abstractmethod
from app.utils.retry import retry_request
from datetime import datetime, time


def get_default_limit_date() -> str:
    now = datetime.now()
    limit_datetime = datetime.combine(now.date(), time(hour=23, minute=0, second=0))
    return limit_datetime.strftime("%Y%m%d%H%M%S")


class SMSProviderInterface(ABC):
    @abstractmethod
    async def send_sms(self, phone: str, message: str) -> dict:
        raise NotImplementedError()


class SMSProvider(SMSProviderInterface):
    BASE_URL = settings.sms_api_url

    async def send_sms(self, phone: str, amount: int, name: str, product_name: str) -> dict:
        limit_date = get_default_limit_date()
        payload = {
            "mid": settings.mid,
            "amount": amount,
            "orderHp": phone,
            "orderName": name,
            "productName": product_name,
            "limitDate": limit_date,
            "hash": self.make_hash(settings.mid, amount, settings.mkey),
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

        return await retry_request(http_call)

    def make_hash(self, mid: str, amount: int, mkey: str) -> str:
        plain_text = f"{mid}{amount}{mkey}"
        return hashlib.sha256(plain_text.encode()).hexdigest()
    

class DummySMSProvider(SMSProviderInterface):
    async def send_sms(self, phone: str, message: str) -> dict:
        return {
            "sms_tid": "SMS" + phone[-4:],
            "status": "sent",
            "provider": "dummy_sms",
            "raw": {"phone": phone, "message": message},
        }
    