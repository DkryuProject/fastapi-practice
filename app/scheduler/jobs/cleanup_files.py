import logging
import os
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.domains.user.models import UserDocument

logger = logging.getLogger("app.jobs.cleanup.files")

def clean_unused_files():
    logger.info("cleanup files job started")
    db: Session = SessionLocal()

    try:
        limit_date = datetime.utcnow() - timedelta(hours=24)
        old_files = db.query(UserDocument).filter(UserDocument.created_at < limit_date).all()

        for doc in old_files:
            if os.path.exists(doc.file_url):
                os.remove(doc.file_url)
            db.delete(doc)

        db.commit()
        logger.info(
            "cleanup files job finished | deleted=%d",
            len(old_files)
        )
    except Exception:
        db.rollback()
        logger.exception("cleanup files job failed")        
    finally:
        db.close()
