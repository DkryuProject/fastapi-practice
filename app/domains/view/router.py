from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.templates import templates
from app.domains.payment.services.payment_service import PaymentService
from datetime import datetime
import hashlib


def sha256_encrypt(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


router = APIRouter()


@router.get("/payment/request/{token}", response_class=HTMLResponse)
def payment_request_view(
    request: Request,
    token: str,
    db: Session = Depends(get_db),
):
    view_data = PaymentService.get_payment_view_by_token(db, token)

    merchant_key = "----"
    merchant_id = "----"

    goods_name = "코페이"
    price = "1004"
    buyer_name = "코페이"
    buyer_tel = "01000000000"
    buyer_email = "test@korpay.com"
    moid = "korpay1234567890"
    return_url = "https://pgapi.korpay.com/returnUrlSample.do"

    edi_date = datetime.now().strftime("%Y%m%d%H%M%S")
    hash_string = sha256_encrypt(
        merchant_id + edi_date + price + merchant_key
    )

    return templates.TemplateResponse(
        "payment_request.html",
        {
            "request": request,
            "merchant_id": merchant_id,
            "goods_name": goods_name,
            "price": price,
            "buyer_name": buyer_name,
            "buyer_tel": buyer_tel,
            "buyer_email": buyer_email,
            "moid": moid,
            "return_url": return_url,
            "edi_date": edi_date,
            "hash_string": hash_string,
        },
    )


@router.get("/request-view/{token}", response_class=HTMLResponse, include_in_schema=False)
def request_view(
        request: Request,
        token: str,
        db: Session = Depends(get_db),
):
    view_data = PaymentService.get_payment_view_by_token(db, token)

    return templates.TemplateResponse(
        "payment_request_back.html",
        {
            "request": request,
            "business_name": "벤티샵",  # 필요시 link에 추가
            "product_name": view_data.product_name,
            "memo": None,
            "purchase_price": view_data.amount,
            #"card_codes": card_codes,
            "token": view_data.token,
            "shop_transaction_id": view_data.order_number,
        },
    )


@router.get("/payment/receipt/{token}", response_class=HTMLResponse)
def receipt_view(
        request: Request,
        token: str,
        db: Session = Depends(get_db),
):
    data = PaymentService.get_receipt_view_data(db, token)

    return templates.TemplateResponse(
        "payment_receipt.html",
        {
            "request": request,
            **data
        }
    )