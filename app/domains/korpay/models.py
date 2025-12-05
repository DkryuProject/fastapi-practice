from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime
from app.core.models_base import TimestampMixin


class PaymentRequest(Base, TimestampMixin):
    __tablename__ = "korpay_payment_request_log"

    id = Column(Integer, primary_key=True, index=True)
    ord_no = Column(String(30), unique=True, index=True, nullable=False)
    mid = Column(String(10), unique=True, index=True, nullable=False)
    goods_amt = Column(String(12))
    card_no = Column(String(13))
    expire_yymm = Column(String(4))
    quota_mon = Column(String(2))
    buyer_nm = Column(String(50))
    goods_nm = Column(String(50))
    ord_hp = Column(String(15))
    res_code = Column(String(4))
    res_msg = Column(String(100))
    app_no = Column(String(16))
    app_date = Column(String(10))
    van_cp_cd = Column(String(10))
    cp_cd = Column(String(2))
    van_iss_cp_cd = Column(String(10))
    iss_cp_cd = Column(String(2))
    tid = Column(String(30))


class PaymentRequestCancel(Base, TimestampMixin):
    __tablename__ = "korpay_payment_request_cancel_log"

    id = Column(Integer, primary_key=True, index=True)
    ord_no = Column(String(30), unique=True, index=True, nullable=False)
    mid = Column(String(10), unique=True, index=True, nullable=False)
    can_amt = Column(String(12))
    can_nm = Column(String(30))
    can_msg = Column(String(100))
    res_code = Column(String(4))
    res_msg = Column(String(100))
    cancel_date = Column(String(8))
    cancel_time = Column(String(6))


class SMSSend(Base, TimestampMixin):
    __tablename__ = "korpay_sms_send_log"

    id = Column(Integer, primary_key=True, index=True)
    mid = Column(String(10), unique=True, index=True, nullable=False)
    limit_date = Column(String(14), nullable=False)
    amount = Column(Integer)
    product_name = Column(String(100))
    order_name = Column(String(30))
    order_hp = Column(String(15))
    rid = Column(String(10))
    result_code = Column(String(4))
    result_message = Column(String(100))
    result_date = Column(String(14))
    response_hash = Column(String(100))
    status = Column(String(10))
