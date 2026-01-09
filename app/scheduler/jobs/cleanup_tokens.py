import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.domains.user.models import RefreshToken

logger = logging.getLogger("app.jobs.cleanup.tokens")

def cleanup_expired_refresh_tokens():
    logger.info("cleanup tokens job started")
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
        logger.info(
            "cleanup tokens job finished | deleted=%d",
            deleted
        )
    except Exception:
        db.rollback()
        logger.exception("cleanup tokens job failed")           
    finally:
        db.close()
