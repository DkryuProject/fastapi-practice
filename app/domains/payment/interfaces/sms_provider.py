import httpx
from abc import ABC, abstractmethod
from app.utils.retry import retry_request


class SMSProviderInterface(ABC):
    BASE_URL = "https://pgapi.korpay.com/api/payment/sms/request"

    @abstractmethod
    async def send_sms(self, phone: str, message: str) -> dict:
        async def http_call():
            async with httpx.AsyncClient(timeout=3) as client:
                resp = await client.post(
                    self.BASE_URL,
                    json={"phone": phone, "msg": message}
                )
                resp.raise_for_status()
                return resp.json()

        return await retry_request(http_call)


class DummySMSProvider(SMSProviderInterface):
    def send_sms(self, phone: str, message: str) -> dict:
        # 실제로는 HTTP 호출 → response parsing
        return {
            "sms_tid": "SMS" + phone[-4:],
            "status": "sent",
            "provider": "dummy_sms",
            "raw": {"phone": phone, "message": message},
        }
