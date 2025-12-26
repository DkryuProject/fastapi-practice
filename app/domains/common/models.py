from sqlalchemy import (
    Column, Integer, String, ForeignKey, Text
)
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.models_base import TimestampMixin


class SMSSendLog(Base, TimestampMixin):
    __tablename__ = "sms_send_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    action = Column(String(100), nullable=False)
    sender = Column(String(20), nullable=False)
    receiver = Column(String(20), nullable=False)
    subject = Column(String(255), nullable=False)
    msg = Column(String(255), nullable=False)
    msg_type = Column(String(10), nullable=False)

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
