from sqlalchemy.orm import Session
from .models import SendLog


def create_send_log(
    db: Session,
    *,
    user_id: int,
    phone: str,
    title: str,
    message: str,
    result_message: str | None,
    result_code: str | None,
    msg_id: str | None,
    error_cnt: int | None,
    success_cnt: int | None,
    msg_type: str | None,
):
    sms_log = SendLog(
        user_id=user_id,
        phone=phone,
        title=title,
        message=message,
        result_message=result_message,
        result_code=result_code,
        msg_id=msg_id,
        error_cnt=error_cnt,
        success_cnt=success_cnt,
        msg_type=msg_type,
    )

    db.add(sms_log)
    return sms_log
