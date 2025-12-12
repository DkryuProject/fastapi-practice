from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.domains.user.schemas import UserSignup
from app.domains.user.service import UserService
from app.core.security import get_current_user
from app.domains.user.models import User

router = APIRouter(prefix="/user", tags=["User"])


# -----------------------------
# 회원가입
# -----------------------------
@router.post("/signup", summary="회원가입")
def signup(payload: UserSignup, db: Session = Depends(get_db)):
    try:
        user = UserService.signup(db, payload)
        return {"message": "회원가입 완료", "user_id": user.id}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/me")
def get_my_info(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name
    }