import os
import base64
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from PIL import Image
from io import BytesIO

from app.domains.payment.interfaces.link_provider import LinkProvider
from app.domains.payment.services.payment_service import PaymentService
from app.domains.payment.services.link_payment_service import LinkPaymentService
from app.domains.payment.schemas import LinkPaymentCreateRequest, LinkPaymentCancelRequest
from app.domains.view.schemas import LinkPaymentViewRequest
from app.core.security import get_current_user
from app.domains.user.models import User

router = APIRouter()

RECEIPT_DIR = "storage/receipt"
os.makedirs(RECEIPT_DIR, exist_ok=True)


async def get_link_provider() -> LinkProvider:
    return LinkProvider()


@router.post("/create", summary="링크 결제 URL 생성")
def create_link_payment(
        data: LinkPaymentCreateRequest,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    payment = PaymentService.create_link_payment(db, data, current_user)

    if not payment:
        raise HTTPException(status_code=500, detail="link create failed")

    return payment


@router.post('/request/{token}', summary="링크 결제 요청 송신")
async def request_link_payment(
        token: str,
        data: LinkPaymentViewRequest,
        db: Session = Depends(get_db)
):
    result = PaymentService.request_link_payment(db, token, data)
    return result


@router.post('/result/{token}', response_class=HTMLResponse, summary="링크 결제 결과 수신")
async def result_link_payment(
        token: str,
        request: Request,
        db: Session = Depends(get_db)
):
    form = await request.form()

    payment = await PaymentService.result_link_payment(
        db=db,
        token=token,
        form=form
    )

    if not payment:
        raise HTTPException(status_code=500, detail="link result failed")

    return {"success": "success"}


@router.post('/cancel', summary="링크 결제 취소")
async def cancel_link_payment(
        payload: LinkPaymentCancelRequest,
        provider: LinkProvider = Depends(get_link_provider),
        db: Session = Depends(get_db)
):
    service = LinkPaymentService(provider)
    payment = await service.cancel_link_payment(db, payload)

    if not payment:
        raise HTTPException(status_code=500, detail="link cancel failed")

    return {"success": "success"}


@router.post("/api/payment/receipt")
async def send_receipt(
        image: str = Form(...),
        phone: str = Form(...),
        shop_transaction_id: str = Form(...)
):
    if not image or not phone or not shop_transaction_id:
        raise HTTPException(status_code=400, detail="필수 값 누락")

    filename = f"{shop_transaction_id}_{phone}.png"
    file_path = os.path.join(RECEIPT_DIR, filename)

    try:
        image_data = image.replace("data:image/png;base64,", "")

        decoded = base64.b64decode(image_data)

        img = Image.open(BytesIO(decoded))

        resized_img = img.resize((640, 1280))

        # 이미지 저장
        resized_img.save(file_path, format="PNG")

        # 이미지 다시 bytes로 변환 (SMS 전송용)
        buffer = BytesIO()
        resized_img.save(buffer, format="PNG")
        image_bytes = buffer.getvalue()

        # SMS 전송

        return {"success": True}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))