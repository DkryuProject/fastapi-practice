from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import crud, schemas
from app.core.security import verify_password
from app.core.jwt import create_access_token, create_refresh_token, decode_token
from app.core.config import settings
from datetime import datetime, timedelta


def signup_user(db: Session, user: schemas.UserCreate):
    exist = crud.get_user_by_email(db, user.email)
    if exist:
        raise HTTPException(status_code=400, detail="Email already exists")
    return crud.create_user(db, user)


def authenticate_user(db: Session, email: str, password: str):
    user = crud.get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def login(db: Session, email: str, password: str):
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_payload = {"sub": str(user.id)}
    access_token = create_access_token(access_payload, expires_delta=settings.access_token_expires)

    refresh_payload = {"sub": str(user.id)}
    refresh_token = create_refresh_token(refresh_payload, expires_delta=settings.refresh_token_expires)

    # store refresh token in DB with expiry
    expires_at = datetime.utcnow() + settings.refresh_token_expires
    crud.create_refresh_token(db, token_str=refresh_token, user_id=user.id, expires_at=expires_at)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user
    }


def refresh_access_token(db: Session, refresh_token: str):
    # decode and verify signature/exp via decode_token
    try:
        payload = decode_token(refresh_token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # ensure token type is refresh
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Token is not a refresh token")

    rt = crud.get_refresh_token(db, refresh_token)
    if not rt or rt.revoked:
        raise HTTPException(status_code=401, detail="Refresh token revoked or not found")

    if rt.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Refresh token expired")

    user = crud.get_user(db, int(payload.get("sub")))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    access_payload = {"sub": str(user.id)}
    access_token = create_access_token(access_payload, expires_delta=settings.access_token_expires)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }
