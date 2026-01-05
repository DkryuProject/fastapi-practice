from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.responses import HTMLResponse

from app.domains.payment.schemas import LinkPaymentCancelRequest
from app.domains.payment.interfaces.link_provider import LinkProviderInterface
from app.domains.payment.services.payment_service import PaymentService


class LinkPaymentService:
    def __init__(self, link_provider: LinkProviderInterface):
        self.link_provider = link_provider

    async def cancel_link_payment(self, db: Session, payload: LinkPaymentCancelRequest):
        result = PaymentService.get_link_payment_result(
            db, payload.id
        )

        if not result:
            raise HTTPException(404, "결제 결과 없음")

        if result.res_cd != "0000":
            raise HTTPException(400, "승인된 결제가 아님")

        payload = {
            "tid": result.tid,
            "canAmt": result.amt,
            "mid": result.request.merchant_id,
            "partCanFlg": "0",
            "payMethod": "card",
            "canId": "ADMIN",
            "canNm": "관리자",
            "canMsg": payload.cancel_reason,
        }
        result = await self.link_provider.cancel(db, payload)

        return {"success": "success"}

    @staticmethod
    def _popup_close_html(shop_transaction_id: str | None = None):
        msg = (
            f"popup-closed?{shop_transaction_id}"
            if shop_transaction_id else "popup-closed"
        )

        return HTMLResponse(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Redirecting...</title>
            <script>
                window.onload = function() {{
                    if (window.opener && !window.opener.closed) {{
                        window.opener.postMessage('{msg}', '*');
                    }}
                    window.close();
                }};
            </script>
        </head>
        <body>
            <p>잠시만 기다려주세요...</p>
        </body>
        </html>
        """)
