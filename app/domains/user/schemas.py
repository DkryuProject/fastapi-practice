from pydantic import BaseModel, EmailStr
from typing import Optional


# -----------------------------
# Signup
# -----------------------------
class UserSignup(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None

    # Profile Info
    phone: Optional[str] = None
    birthday: Optional[str] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    address_detail: Optional[str] = None
    zipcode: Optional[str] = None

    # Business Info
    business_name: Optional[str] = None
    business_number: Optional[str] = None
    ceo_name: Optional[str] = None
    business_type: Optional[str] = None
    business_item: Optional[str] = None
    tel: Optional[str] = None
    business_address: Optional[str] = None
    business_address_detail: Optional[str] = None
    business_zipcode: Optional[str] = None


# -----------------------------
# Login
# -----------------------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# -----------------------------
# Token Response
# -----------------------------
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
