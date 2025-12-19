import httpx
import hashlib
from app.core.config import settings
from abc import ABC, abstractmethod
from app.utils.retry import retry_request
from app.domains.payment.schemas import ManualPaymentResult, ManualPaymentRequest


def make_hash(mid: str, amount: int) -> str:
    plain_text = f"{mid}{amount}"
    return hashlib.sha256(plain_text.encode()).hexdigest()


class ManualProviderInterface(ABC):
    @abstractmethod
    async def approve(self, order_number: str, data: ManualPaymentRequest) -> ManualPaymentResult:
        raise NotImplementedError()


class ManualProvider(ManualProviderInterface):
    BASE_URL = settings.manual_api_url

    async def approve(self, order_number: str, data: ManualPaymentRequest) -> ManualPaymentResult:
        expire_yymm = f"{int(data.expire_year) % 100:02d}{int(data.expire_month):02d}"

        payload = {
            "ordNo": order_number,
            "mid": settings.mid,
            "mkey": settings.mkey,
            "goodsAmt": data.amount,
            "cardNo": data.card_number,
            "expireYymm": expire_yymm,
            "quotaMon": data.quota,
            "buyer_nm": data.buyer_name,
            "goodsNm": data.goods_name,
            "ordHp": data.phone,
            "hash": make_hash(settings.mid, data.amount),
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

        return ManualPaymentResult(
            tid=raw.get("TID"),
            code=raw.get("res_code"),
            message=raw.get("res_msg"),
            app_number=raw.get("APP_NO"),
            app_date=raw.get("APP_DATE"),
            van_cp_cd=raw.get("VAN_CP_CD"),
            cp_cd=raw.get("CP_CD"),
            van_iss_cp_cd=raw.get("VAN_ISS_CP_CD"),
            iss_cp_cd=raw.get("ISS_CP_CD"),
        )
    