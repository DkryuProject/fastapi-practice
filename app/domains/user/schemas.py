from pydantic import BaseModel, EmailStr
from typing import Optional, List
from app.domains.user.models import UserStatusEnum


# -----------------------------
# User Profile Info Schema
# -----------------------------
class UserProfileInfoSchema(BaseModel):
    email: EmailStr
    phone: str
    address: str
    address_detail: str
    zipcode: str


# -----------------------------
# Business Info Schema
# -----------------------------
class UserBusinessInfoSchema(BaseModel):
    business_name: str
    business_number: str
    ceo_name: str
    business_type: str
    business_item: str
    tel: str
    business_address: str
    business_address_detail: str
    business_zipcode: str


# -----------------------------
# Bank Info Schema
# -----------------------------
class UserBankInfoSchema(BaseModel):
    bank_name: str
    account_number: str
    holder_name: str


# -----------------------------
# Document Schema
# -----------------------------
class UserDocumentSchema(BaseModel):
    doc_type: str  


# -----------------------------
# Signup
# -----------------------------
class UserSignup(BaseModel):
    user_id: str
    password: str
    name: Optional[str] = None
    adult_agree_yn: bool
    my_info_agree_yn: bool
    service_agree_yn: bool
    special_agree_yn: bool
    marketing_agree_yn: bool

    profile: Optional[UserProfileInfoSchema] = None
    business: Optional[UserBusinessInfoSchema] = None
    bank_info: Optional[UserBankInfoSchema] = None
    documents: Optional[List[UserDocumentSchema]] = None

    class Config:
        arbitrary_types_allowed = True


# -----------------------------
# Login
# -----------------------------
class UserLogin(BaseModel):
    user_id: str
    password: str


# -----------------------------
# Token Response
# -----------------------------
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# -----------------------------
# 아이디 찾기
# -----------------------------
class FindUserIDRequest(BaseModel):
    email: EmailStr
    phone: str


class FindUserIDResponse(BaseModel):
    user_id: str


# -----------------------------
# 비밀번호 찾기
# -----------------------------
class ResetPasswordRequest(BaseModel):
    user_id: str
    email: EmailStr
    phone: str


class ResetPasswordResponse(BaseModel):
    message: str


# -----------------------------
# 비밀번호 변경
# -----------------------------
class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


class ChangePasswordResponse(BaseModel):
    message: str


# -----------------------------
# 토큰 
# -----------------------------
class PushTokenRequest(BaseModel):
    token: str
    device_id: str
    platform: str  # ios / android / web


class PushTokenResponse(BaseModel):
    message: str


# -----------------------------
# 유저 상태 변경
# -----------------------------
class ChangeUserStatusRequest(BaseModel):
    status: UserStatusEnum


class ChangeUserStatusResponse(BaseModel):
    message: str
    user_id: int
    new_status: UserStatusEnum
