from sqlalchemy.orm import Session
from app.domains.user.crud import UserCRUD
from app.domains.common.schemas import (
    SMSSendRequest,
    KakaoSendRequest,
)
from app.domains.user.models import User
from app.core.exceptions import AppException
from app.domains.common.service import CommonService

import logging
logger = logging.getLogger(__name__)


class CommonService:
    @staticmethod
    def save_sms_send_log(db: Session, data: SMSSendRequest, user: User):
        try:
            CommonService.save_sms_send_log(db=db, user_id=user.id, data=data)
            db.commit()

            return {
                "code": 1,
                "message": "저장에 성공하였습니다."
            }

        except Exception as e:
            db.rollback()
            logger.exception("로그 저장 실패: %s", e)
            raise AppException("로그 저장에 실패하였습니다.", 500)

    @staticmethod
    def save_kakao_send_log(db: Session, data: KakaoSendRequest, user: User):
        try:
            CommonService.save_kakao_send_log(db=db, user_id=user.id, data=data)
            db.commit()
            
            return {
                "code": 1,
                "message": "저장에 성공하였습니다."
            }

        except Exception as e:
            db.rollback()
            logger.exception("로그 저장 실패: %s", e)
            raise AppException("로그 저장에 실패하였습니다.", 500)    
                