from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.domains.user.schemas import UserLogin, TokenResponse
from app.domains.user.service import UserService

router = APIRouter()


# -----------------------------
# 로그인
# -----------------------------
@router.post("/login", response_model=TokenResponse, summary="로그인")
def login(payload: UserLogin, db: Session = Depends(get_db)):
    try:
        tokens = UserService.login(db, payload.user_id, payload.password)
        return tokens
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# -----------------------------
# Refresh Token 재발급
# -----------------------------
@router.post("/refresh", response_model=TokenResponse, summary="토큰 재발급")
def refresh(refresh_token: str, db: Session = Depends(get_db)):
    try:
        tokens = UserService.refresh_tokens(db, refresh_token)
        return tokens
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


# -----------------------------
# Logout
# -----------------------------
@router.post("/logout", summary="로그아웃 (Refresh Token 폐기)")
def logout(refresh_token: str, db: Session = Depends(get_db)):
    try:
        UserService.logout(db, refresh_token)
        return {"message": "로그아웃 완료"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
