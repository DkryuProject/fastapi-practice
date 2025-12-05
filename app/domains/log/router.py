from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from .crud import get_logs
from .schemas import UserActionLogResponse
from app.domains.auth.router import get_current_user

router = APIRouter()

@router.get("/", response_model=list[UserActionLogResponse])
def logs(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return get_logs(db, user_id=current_user.id)
