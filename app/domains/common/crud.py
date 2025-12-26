from sqlalchemy.orm import Session
from datetime import datetime
from app.domains.common.models import (
    SMSSendLog,
    KakaoSendLog,
)
from app.domains.common.schemas import (
    SMSSendRequest,
    KakaoSendRequest,
)


class CommonCRUD:
    @staticmethod
    def save_sms_send_log(db: Session, user_id: int, data: SMSSendRequest):
        log = SMSSendLog(
            user_id=user_id,
            action=data.action,
            sender=data.sender,
            receiver=data.receiver,
            subject=data.subject,
            msg=data.msg,
            msg_type=data.msg_type,
        )
        db.add(log)
        return log

    @staticmethod
    def save_kakao_send_log(db: Session, user_id: int, data: KakaoSendRequest):
        log = KakaoSendLog(
            user_id=user_id,
            tpl_code=data.tpl_code,
            sender=data.sender,
            emtitle_1=data.emtitle_1,
            subject=data.subject,
            receiver_1=data.receiver_1,
            message_1=data.message_1,
            button_1=data.button_1,
        )
        db.add(log)
        return log    
    