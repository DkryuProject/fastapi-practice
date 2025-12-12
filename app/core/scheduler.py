from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import SessionLocal
from app.domains.user.models import RefreshToken


def cleanup_expired_refresh_tokens():
    db: Session = SessionLocal()
    now = datetime.utcnow()

    # 만료 or revoked 된 토큰 삭제
    deleted = (
        db.query(RefreshToken)
        .filter(
            (RefreshToken.expires_at <= now) |
            (RefreshToken.revoked == True)
        )
        .delete(synchronize_session=False)
    )

    db.commit()
    db.close()

    print(f"[Cron] Deleted {deleted} expired or revoked refresh tokens")


scheduler = BackgroundScheduler()


def start_scheduler():
    # 1시간 주기 실행
    scheduler.add_job(
        cleanup_expired_refresh_tokens,
        "interval",
        hours=1,
        id="cleanup_refresh_tokens",
        replace_existing=True
    )
    scheduler.start()
