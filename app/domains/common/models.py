from sqlalchemy import (
    Column, Integer, String, ForeignKey, Text
)
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.models_base import TimestampMixin


class SendLog(Base, TimestampMixin):
    __tablename__ = "send_logs"

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

    user = relationship("User", back_populates="send_logs")
