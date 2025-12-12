from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.domains.user.schemas import (
    UserSignup, 
    FindUserIDRequest, 
    FindUserIDResponse, 
    ResetPasswordRequest, 
    ResetPasswordResponse,
    ChangePasswordRequest,
    ChangePasswordResponse,
    PushTokenRequest,
    PushTokenResponse,
    ChangeUserStatusRequest,
    ChangeUserStatusResponse
    )
from app.domains.user.service import UserService
from app.core.security import get_current_user
from app.domains.user.models import User
from app.core.exceptions import AppException

router = APIRouter()


# -----------------------------
# 회원가입
# -----------------------------
@router.post("/signup", summary="회원가입")
def signup(
    # -----------------------------
    # 기본 회원 정보
    # -----------------------------
    user_id: str = Form(...),
    password: str = Form(...),
    name: Optional[str] = Form(None),
    adult_agree_yn: bool = Form(...),
    my_info_agree_yn: bool = Form(...),
    service_agree_yn: bool = Form(...),
    special_agree_yn: bool = Form(...),
    marketing_agree_yn: bool = Form(...),

    # -----------------------------
    # Profile Info
    # -----------------------------
    email: str = Form(...),
    phone: str = Form(...),
    birthday: str = Form(...),
    gender: str = Form(...),
    address: str = Form(...),
    address_detail: str = Form(...),
    zipcode: str = Form(...),

    # -----------------------------
    # Business Info
    # -----------------------------
    business_name: str = Form(...),
    business_number: str = Form(...),
    ceo_name: str = Form(...),
    business_type: str = Form(...),
    business_item: str = Form(...),
    tel: str = Form(...),
    business_address: str = Form(...),
    business_address_detail: str = Form(...),
    business_zipcode: str = Form(...),

    # -----------------------------
    # Bank Info
    # -----------------------------
    bank_name: str = Form(...),
    account_number: str = Form(...),
    holder_name: str = Form(...),

    # -----------------------------
    # Documents metadata + file
    # -----------------------------
    doc_types: List[str] = Form(...),     

    files: List[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    try:
        # -----------------------------
        # Pydantic 객체 생성
        # -----------------------------
        signup_data = UserSignup(
            user_id=user_id,
            password=password,
            name=name,
            adult_agree_yn=adult_agree_yn,
            my_info_agree_yn=my_info_agree_yn,
            service_agree_yn=service_agree_yn,
            special_agree_yn=special_agree_yn,
            marketing_agree_yn=marketing_agree_yn,

            profile={
                "email": email,
                "phone": phone,
                "birthday": birthday,
                "gender": gender,
                "address": address,
                "address_detail": address_detail,
                "zipcode": zipcode
            },

            business={
                "business_name": business_name,
                "business_number": business_number,
                "ceo_name": ceo_name,
                "business_type": business_type,
                "business_item": business_item,
                "tel": tel,
                "business_address": business_address,
                "business_address_detail": business_address_detail,
                "business_zipcode": business_zipcode
            },

            bank_info={
                "bank_name": bank_name,
                "account_number": account_number,
                "holder_name": holder_name
            },

            documents=[{"doc_type": dt} for dt in doc_types]
        )

        user = UserService.signup(db, signup_data, files)

        return {"message": "회원가입 완료", "user_id": user.id}
    
    except Exception as e:
        raise AppException(str(e), 400)


@router.get("/me", summary="내 정보")
def get_my_info(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name
    }

@router.post("/find-id", response_model=FindUserIDResponse)
def find_user_id(req: FindUserIDRequest, db: Session = Depends(get_db)):
    user_id = UserService.find_user_id(db, req)
    return FindUserIDResponse(user_id=user_id)


@router.post("/reset-password", response_model=ResetPasswordResponse)
def reset_password(req: ResetPasswordRequest, db: Session = Depends(get_db)):
    temp_pw = UserService.reset_password(db, req)
    return ResetPasswordResponse(message="임시 비밀번호가 이메일로 발송되었습니다.")


@router.post("/change-password", response_model=ChangePasswordResponse)
def change_password(req: ChangePasswordRequest, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    msg = UserService.change_password(db, current_user, req.old_password, req.new_password)
    return ChangePasswordResponse(message=msg)


@router.post("/save-push-token", response_model=PushTokenResponse)
def save_push_token(req: PushTokenRequest, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    UserService.save_token(db, current_user.id, req.token, req.device_id, req.platform)
    return PushTokenResponse(message="푸시 토큰 저장 완료")


@router.delete("/delete-push-token", response_model=PushTokenResponse)
def delete_push_token(req: PushTokenRequest, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    UserService.remove_token(db, current_user.id, req.token)
    return PushTokenResponse(message="푸시 토큰 삭제 완료")

@router.patch("/change-status", response_model=ChangeUserStatusResponse)
def change_status(req: ChangeUserStatusRequest, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    user = UserService.change_user_status(db, current_user, req.status)
    return ChangeUserStatusResponse(
        message="상태 변경 완료",
        user_id=user.id,
        new_status=user.status
    )
