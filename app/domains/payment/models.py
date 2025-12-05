from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime
from app.core.models_base import TimestampMixin


class Payment(Base, TimestampMixin):
    __tablename__ = "payment"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(30), unique=True, index=True, nullable=False)
    type = Column(String(10), nullable=False)
    amount = Column(String(12), nullable=False)
    product_name = Column(String(100))
    order_name = Column(String(100))
    phone = Column(String(50))
    status = Column(String(10), nullable=False)
