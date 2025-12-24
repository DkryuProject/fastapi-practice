from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.responses import HTMLResponse

from app.domains.view.schemas import LinkPaymentViewRequest
from app.domains.payment.schemas.payment_schemas import PaymentCreate, PaymentLogCreate
from app.domains.payment.interfaces.link_provider import LinkProviderInterface
from app.domains.payment.services.payment_service import PaymentService


class LinkPaymentService:
    def __init__(self, link_provider: LinkProviderInterface):
        self.link_provider = link_provider

    async def request(self, db: Session, token: str, data: LinkPaymentViewRequest):
        link = PaymentService.get_payment_view_by_token(db, token)

        payment = link.payment

        PaymentService.update_status(db, payment, "PENDING")

        try:
            result = await self.link_provider.request(db, payment, data)

            PaymentService.update_status(db, payment, "SUCCESS")

        except Exception as e:
            PaymentService.update_status(db, payment, "ERROR")
            raise e

        return result

    async def handle_link_payment_result(self, db, token: str, params):
        required = ["resCd", "resMsg", "certControlNo", "shop_transaction_id"]
        for key in required:
            if key not in params:
                return LinkPaymentService._popup_close_html()

        if params["resCd"] != "0000":
            raise HTTPException(status_code=401, detail=params["resMsg"])

        link = PaymentService.get_payment_view_by_token(db, token)
        if not link:
            raise HTTPException(status_code=404, detail="잘못된 링크")

        payment_enroll = PaymentService.get_link_request_by_shop_transaction_id(
            db, params["shop_transaction_id"]
        )
        if not payment_enroll:
            raise HTTPException(status_code=404, detail="payment not found")

        result = await self.link_provider.result(db, payment_enroll)

        return LinkPaymentService._popup_close_html(
            payment_enroll.shop_transaction_id
        )

    async def cancel_link_payment(self, db: Session, shop_transaction_id: str):
        # 1. 승인 결과 조회
        result = PaymentService.get_payment_result(
            db, shop_transaction_id
        )

        if not result:
            raise HTTPException(status_code=404, detail="payment not found")

        if result.res_cd != "0000":
            raise HTTPException(
                status_code=400,
                detail="payment is not approved"
            )

        result = await self.link_provider.cancel(db, result)

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
