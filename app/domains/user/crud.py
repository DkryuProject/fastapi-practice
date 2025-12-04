from sqlalchemy.orm import Session
from . import models, schemas
from app.core.security import hash_password
from datetime import datetime, timedelta
from app.core.config import settings


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email,
        password=hash_password(user.password),
        name=user.name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session):
    return db.query(models.User).all()


# Refresh token CRUD
def create_refresh_token(db: Session, token_str: str, user_id: int, expires_at: datetime):
    rt = models.RefreshToken(
        token=token_str,
        user_id=user_id,
        expires_at=expires_at
    )
    db.add(rt)
    db.commit()
    db.refresh(rt)
    return rt


def get_refresh_token(db: Session, token_str: str):
    return db.query(models.RefreshToken).filter(models.RefreshToken.token == token_str).first()


def revoke_refresh_token(db: Session, token_str: str):
    rt = get_refresh_token(db, token_str)
    if rt:
        rt.revoked = True
        db.add(rt)
        db.commit()
    return rt


def revoke_all_user_refresh_tokens(db: Session, user_id: int):
    db.query(models.RefreshToken).filter(models.RefreshToken.user_id == user_id).update({"revoked": True})
    db.commit()
