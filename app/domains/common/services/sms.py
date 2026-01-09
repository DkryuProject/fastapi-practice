import os
import httpx
from sqlalchemy.orm import Session
from app.core.exceptions import AppException
from app.core.config import settings
from ..crud import create_send_log


ALIGO_SEND_URL = "https://apis.aligo.in/send/"
ALIGO_LIST_URL = "https://apis.aligo.in/list/"

import logging
logger = logging.getLogger(__name__)


class Sms:
    @staticmethod
    async def send(
        db: Session,
        user_id: int,
        phone: str,
        title: str,
        message: str
    ):
        try:
            async with httpx.AsyncClient(verify=False) as client:
                response = await client.post(
                    ALIGO_SEND_URL,
                    data={
                        "key": settings.SMS_SEND_KEY,
                        "userid": settings.SMS_SEND_ID,
                        "msg": message,
                        "receiver": phone,
                        "sender": settings.SMS_SEND_NUMBER,
                        "title": title,
                        "msg_type": "sms",
                    }
                )

            body = response.json()

            create_send_log(
                db,
                user_id=user_id,
                phone=phone,
                title=title,
                message=message,
                result_message=body.get("message"),
                result_code=body.get("result_code"),
                msg_id=body.get("msg_id"),
                error_cnt=body.get("error_cnt"),
                success_cnt=body.get("success_cnt"),
                msg_type=body.get("msg_type"),
            )

            db.commit()

            return {
                "result_code": body.get("result_code"),
                "message": body.get("message"),
                "msg_id": body.get("msg_id"),
            }       
         
        except Exception as e:
            db.rollback()
            logger.exception("SMS 발송 실패: %s", e)
            raise AppException("SMS 발송에 실패하였습니다.", 500)
