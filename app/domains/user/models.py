import enum
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base
from app.core.models_base import TimestampMixin


class UserStatusEnum(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"


# -----------------------------
# User
# -----------------------------
class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(50), nullable=True)
    adult_agree_yn = Column(Boolean, nullable=True)
    my_info_agree_yn = Column(Boolean, nullable=True)
    service_agree_yn = Column(Boolean, nullable=True)
    special_agree_yn = Column(Boolean, nullable=True)
    marketing_agree_yn = Column(Boolean, nullable=True)
    status = Column(Enum(UserStatusEnum), nullable=False, default=UserStatusEnum.SUSPENDED)

    last_login_time = Column(DateTime, nullable=True)
    last_login_ip = Column(String(50), nullable=True)

    refresh_tokens = relationship("RefreshToken", back_populates="user")
    profile = relationship("UserProfile", uselist=False, back_populates="user")
    business = relationship("UserBusiness", uselist=False, back_populates="user")
    push_settings = relationship("UserPushSetting", uselist=False, back_populates="user")
    push_tokens = relationship("UserPushToken", back_populates="user")
    bank_info = relationship("UserBankInfo", uselist=False, back_populates="user")
    documents = relationship("UserDocument", back_populates="user")
    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")


# -----------------------------
# Refresh Token
# -----------------------------
class RefreshToken(Base, TimestampMixin):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), nullable=False, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    issued_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    revoked = Column(Boolean, default=False)

    user = relationship("User", back_populates="refresh_tokens")


# -----------------------------
# User Profile (개인정보)
# -----------------------------
class UserProfile(Base, TimestampMixin):
    __tablename__ = "user_profile"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    email = Column(String(255), unique=True, index=True, nullable=False)

    phone = Column(String(20), nullable=True)

    address = Column(String(255), nullable=True)
    address_detail = Column(String(255), nullable=True)
    zipcode = Column(String(20), nullable=True)

    user = relationship("User", back_populates="profile")


# -----------------------------
# User Business (사업자 정보)
# -----------------------------
class UserBusiness(Base, TimestampMixin):
    __tablename__ = "user_business"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)

    business_name = Column(String(100))
    business_number = Column(String(20), index=True)
    ceo_name = Column(String(50))
    business_type = Column(String(50))
    business_item = Column(String(50))

    tel = Column(String(30))
    address = Column(String(255))
    address_detail = Column(String(255))
    zipcode = Column(String(20))

    user = relationship("User", back_populates="business")


# -----------------------------
# User Push Setting
# -----------------------------
class UserPushSetting(Base, TimestampMixin):
    __tablename__ = "user_push_setting"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)

    allow_marketing = Column(Boolean, default=False)
    allow_noti = Column(Boolean, default=True)

    user = relationship("User", back_populates="push_settings")


# -----------------------------
# User Push Token (디바이스)
# -----------------------------
class UserPushToken(Base, TimestampMixin):
    __tablename__ = "user_push_token"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    device_id = Column(String(255), nullable=True)
    token = Column(Text, nullable=False)
    platform = Column(String(20))  # ios / android / web
    revoked = Column(Boolean, default=False)

    user = relationship("User", back_populates="push_tokens")


# -----------------------------
# User Action Log
# -----------------------------
class UserActionLog(Base, TimestampMixin):
    __tablename__ = "user_action_log"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    action = Column(String(100), nullable=False)
    endpoint = Column(String(255), nullable=False)
    method = Column(String(10), nullable=False)
    client_ip = Column(String(100), nullable=True)
    user_agent = Column(Text, nullable=True)

    user = relationship("User")


# -----------------------------
# User Bank Info (은행정보)
# -----------------------------
class UserBankInfo(Base, TimestampMixin):
    __tablename__ = "user_bank_info"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)

    bank_name = Column(String(100), nullable=False)
    account_number = Column(String(50), nullable=False)
    holder_name = Column(String(50), nullable=False)

    user = relationship("User", back_populates="bank_info")


# -----------------------------
# User Document (유저 문서)
# -----------------------------
class UserDocument(Base, TimestampMixin):
    __tablename__ = "user_document"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    doc_type = Column(String(50), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_url = Column(String(500), nullable=False)
    file_hash = Column(String(500), index=True)
    file_size = Column(Integer)
    ext = Column(String(50))

    user = relationship("User", back_populates="documents")


# -----------------------------
# 업로드 히스토리 
# -----------------------------
class UploadHistory(Base, TimestampMixin):
    __tablename__ = "upload_history"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255))
    file_hash = Column(String(500))
    status = Column(String(20))
    reason = Column(String(255), nullable=True)
