from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.main import templates
from app.domains.payment.services.payment_service import PaymentService

router = APIRouter()


@router.get("/request-view/{token}", response_class=HTMLResponse)
def request_view(
        request: Request,
        token: str,
        db: Session = Depends(get_db),
):
    view_data = PaymentService.get_payment_view_by_token(db, token)

    return templates.TemplateResponse(
        "payment_request.html",
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