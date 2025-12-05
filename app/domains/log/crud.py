from sqlalchemy.orm import Session
from .models import UserActionLog
from datetime import datetime

def create_log(
    db: Session,
    *,
    user_id: int | None,
    action: str,
    endpoint: str,
    method: str,
    client_ip: str | None,
    user_agent: str | None,
):
    log = UserActionLog(
        user_id=user_id,
        action=action,
        endpoint=endpoint,
        method=method,
        client_ip=client_ip,
        user_agent=user_agent,
    )
    db.add(log)
    db.commit()
    return log

def get_logs(db: Session, user_id: int | None = None):
    query = db.query(UserActionLog)
    if user_id:
        query = query.filter(UserActionLog.user_id == user_id)
    return query.order_by(UserActionLog.id.desc()).all()
