from apscheduler.schedulers.background import BackgroundScheduler
import os
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.domains.user.models import UserDocument
from app.domains.user.models import RefreshToken

UPLOAD_DIR = "uploads"
FILE_LIFETIME_DAYS = 7


def clean_unused_files():
    db: Session = SessionLocal()

    try:
        limit_date = datetime.utcnow() - timedelta(hours=24)
        old_files = db.query(UserDocument).filter(UserDocument.created_at < limit_date).all()

        for doc in old_files:
            if os.path.exists(doc.file_url):
                os.remove(doc.file_url)
            db.delete(doc)

        db.commit()
    finally:
        db.close()

def cleanup_expired_refresh_tokens():
    db: Session = SessionLocal()

    try:
        now = datetime.utcnow()

        deleted = (
            db.query(RefreshToken)
            .filter(
                (RefreshToken.expires_at <= now) |
                (RefreshToken.revoked == True)
            )
            .delete(synchronize_session=False)
        )

        db.commit()
    finally:
        db.close()


scheduler = BackgroundScheduler()

def start_scheduler():
    scheduler.add_job(cleanup_expired_refresh_tokens, "interval", hours=1, id="cleanup_refresh_tokens", replace_existing=True)  
    scheduler.add_job(clean_unused_files, "interval", hours=6, id="clean_unused_files")
    scheduler.start()