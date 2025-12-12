from pydantic import BaseModel, EmailStr
from typing import Optional, List


# -----------------------------
# User Profile Info Schema
# -----------------------------
class UserProfileInfoSchema(BaseModel):
    email: EmailStr
    phone: str
    birthday: str
    gender: str
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
    uaer_id: str
    password: str


# -----------------------------
# Token Response
# -----------------------------
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
