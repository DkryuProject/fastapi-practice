from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.domains.user import service as user_service, crud as user_crud, schemas as user_schemas
from app.core.jwt import decode_token
from app.core.config import settings
from datetime import datetime

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/login", response_model=user_schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    res = user_service.login(db, form_data.username, form_data.password)
    return {
        "access_token": res["access_token"],
        "refresh_token": res["refresh_token"],
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=user_schemas.Token)
def refresh(refresh_token: str, db: Session = Depends(get_db)):
    res = user_service.refresh_access_token(db, refresh_token)
    return {
        "access_token": res["access_token"],
        "refresh_token": res["refresh_token"],
        "token_type": "bearer"
    }


@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_db)):
    rt = user_crud.revoke_refresh_token(db, refresh_token)
    if not rt:
        raise HTTPException(status_code=400, detail="Refresh token not found")
    return {"detail": "Logged out"}


# Dependency to get current user from access token
from fastapi import Request
from app.domains.user import crud


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    if payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not an access token")

    user_id = int(payload.get("sub"))
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/me", response_model=user_schemas.UserResponse)
def me(current_user=Depends(get_current_user)):
    return current_user
