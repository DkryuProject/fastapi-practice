from sqlalchemy import (
    Column, Integer, String, ForeignKey, Text
)
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.models_base import TimestampMixin


class SMSLog(Base, TimestampMixin):
    __tablename__ = "sms_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    phone = Column(String(20), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(String(255), nullable=False)
    msg_type = Column(String(10), nullable=False)

    result_code = Column(Integer, nullable=False)
    result_message = Column(String(255))
    msg_id = Column(Integer)
    success_cnt = Column(Integer)
    error_cnt = Column(Integer)

    user = relationship("User", back_populates="sms_send_logs")


class KakaoSendLog(Base, TimestampMixin):
    __tablename__ = "kakao_send_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    tpl_code = Column(String(100), nullable=False)
    sender = Column(String(20), nullable=False)
    emtitle_1 = Column(String(20), nullable=False)
    subject = Column(String(255), nullable=False)
    receiver_1 = Column(String(255), nullable=False)
    message_1 = Column(String(255), nullable=False)
    button_1 = Column(Text, nullable=False)

    user = relationship("User", back_populates="kakao_send_logs")
