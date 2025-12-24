import httpx
import base64
from datetime import datetime

from sqlalchemy.orm import Session
from abc import ABC, abstractmethod
from app.utils.retry import retry_request
from app.domains.payment.models import Payment
from app.domains.view.schemas import LinkPaymentViewRequest
from app.core.config import settings
from app.domains.payment.services.payment_service import PaymentService


class LinkProviderInterface(ABC):
    @abstractmethod
    async def request(self, db: Session, payment: Payment, data: LinkPaymentViewRequest) -> dict:
        raise NotImplementedError()

    @abstractmethod
    async def result(self, db: Session, payment: Payment, data: LinkPaymentViewRequest) -> dict:
        raise NotImplementedError()

    @abstractmethod
    async def cancel(self, db: Session, payment: Payment, data: LinkPaymentViewRequest) -> dict:
        raise NotImplementedError()


class LinkProvider(LinkProviderInterface):
    async def request(self, db: Session, payment: Payment, data: LinkPaymentViewRequest) -> dict:
        shop_req_date = datetime.now().strftime("%Y%m%d%H%M%S")
        shop_order_no = f"prd{datetime.now().strftime('%y%m%d%H%M%S')}"
        tax = payment.amount * 0.1

        business = payment.user.business

        payload = {
            "shopTransactionId": payment.order_number,
            'shopReqDate': shop_req_date,
            'vanTid': business.tid,
            'shopOrderNo': shop_order_no,
            'amount': payment.amount,
            'tax': tax,
            'returnUrl': f"{settings.APP_URL}/api/v1/payment/link/result/{payment.link_create.token}",
            'productNm': data.product_name,
            'mallNm': business.business_name,
            'bussNo': business.business_number.replace("-", ""),
            'cardCode': data.card_code,
            'installment': data.installment,
            'clientOs': data.client_os,
        }

        headers = {
            "Authorization": "Basic " + base64.b64encode(
                business.tid.encode()
            ).decode(),
            "Content-Type": "application/json",
            "Charset": "euc-kr",
        }

        async def http_call():
            async with httpx.AsyncClient(timeout=3) as client:
                resp = await client.post(
                    "https://api.kicc.co.kr/appcardpay/v1/transactions.do",
                    json=payload,
                    headers=headers,
                )
                resp.raise_for_status()
                return resp.json()

        raw = await retry_request(http_call)

        if raw.get("resCd") != "0000":
            raise ValueError(raw.get("resMsg", "결제 요청 실패"))

        cert_page_url = raw["certPageUrl"]
        result = PaymentService.request_link_payment(db, payment.id, payload, cert_page_url)

        return {
            "redirect_url": cert_page_url
        }

    async def result(self, db: Session, payment: Payment, data: LinkPaymentViewRequest) -> dict:
        headers = {
            "Authorization": "Basic " + base64.b64encode(
                payment_enroll.van_tid.encode()
            ).decode(),
            "Content-Type": "application/json",
            "Charset": "euc-kr",
        }

        payload = {
            "shopTransactionId": payment_enroll.shop_transaction_id,
            "approvalReqDate": datetime.now().strftime("%Y%m%d"),
            "vanTid": payment_enroll.van_tid,
            "certControlNo": params["certControlNo"],
        }

        async def http_call():
            async with httpx.AsyncClient(timeout=3) as client:
                resp = await client.post(
                    "https://api.kicc.co.kr/appcardpay/v1/approval.do",
                    json=payload,
                    headers=headers,
                )
                resp.raise_for_status()
                return resp.json()

        body = await retry_request(http_call)

        if body.get("resCd") != "0000":
            raise ValueError(body.get("resMsg"))

        PaymentCRUD.create_payment_result(db, body)

        return {

        }

    async def cancel(self, db: Session, payment: Payment, data: LinkPaymentViewRequest) -> dict:
        headers = {
            "Authorization": "Basic " + base64.b64encode(
                result.van_tid.encode()
            ).decode(),
            "Content-Type": "application/json",
            "Charset": "euc-kr",
        }

        payload = {
            "shopTransactionId": f"italkpay{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "approvalReqDate": datetime.now().strftime("%Y%m%d"),
            "vanTid": result.van_tid,
            "controlNo": result.cert_controll_no,
            "cancelReqDate": datetime.now().strftime("%Y%m%d"),
        }

        async def http_call():
            async with httpx.AsyncClient(timeout=3) as client:
                resp = await client.post(
                    "https://api.kicc.co.kr/appcardpay/v1/cancel.do",
                    json=payload,
                    headers=headers,
                )
                resp.raise_for_status()
                return resp.json()

        body = await retry_request(http_call)

        if body.get("resCd") != "0000":
            raise ValueError(body.get("resMsg"))

        # 3. 취소 결과 저장
        PaymentCRUD.create_payment_cancel(db, body, result)

        return {

        }