from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.domains.common.schemas import SMSSendRequest, KakaoSendRequest
from app.core.security import get_current_user
from .services import sms_service


router = APIRouter()


@router.post("/sms/send", summary="SMS 전송")
async def send_sms(
    data: SMSSendRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await sms_service.send(db, current_user.id, data.phone, data.title, data.message)
