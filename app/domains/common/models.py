from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum
)
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.models_base import TimestampMixin


class SMSSendLog(Base, TimestampMixin):
    __tablename__ = "sms_send_log"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)

    action = Column(String(100), nullable=False)
    sender = Column(String(20), nullable=False)
    receiver = Column(String(20), nullable=False)
    subject = Column(String(255), nullable=False)
    msg = Column(String(255), nullable=False)
    msg_type = Column(String(10), nullable=False)

    user = relationship("User", back_populates="sms_send_log")