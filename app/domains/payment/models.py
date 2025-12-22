from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.models_base import TimestampMixin


class Payment(Base, TimestampMixin):
    __tablename__ = "payment"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(30), unique=True, nullable=False, index=True)

    type = Column(String(20), nullable=False)
    amount = Column(Integer, nullable=False)
    status = Column(String(20), default="request")
    interface_status = Column(String(20), default="INIT")

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    sms_detail = relationship("PaymentSMS", back_populates="payment", uselist=False, cascade="all, delete-orphan")
    manual_card_detail = relationship("PaymentManual", back_populates="payment", uselist=False, cascade="all, delete-orphan")
    cash_receipt_detail = relationship("PaymentCashReceipt", back_populates="payment", uselist=False, cascade="all, delete-orphan")
    link_request = relationship("PaymentLinkRequest", back_populates="payment", uselist=False, cascade="all, delete-orphan")
    link_result = relationship("PaymentLinkResult", back_populates="payment", uselist=False, cascade="all, delete-orphan")
    link_cancel = relationship("PaymentLinkCancel", back_populates="payment", uselist=False, cascade="all, delete-orphan")
    link_enroll = relationship("PaymentLinkEnroll", back_populates="payment", uselist=False, cascade="all, delete-orphan")
    
    logs = relationship("PaymentLog", back_populates="payment", cascade="all, delete-orphan")
    user = relationship("User", back_populates="payments")


class PaymentSMS(Base, TimestampMixin):
    __tablename__ = "payment_sms"

    id = Column(Integer, primary_key=True)
    payment_id = Column(Integer, ForeignKey("payment.id"), unique=True)

    product_name = Column(String(100))
    order_name = Column(String(30))
    amount = Column(Integer)
    phone = Column(String(50))

    rid = Column(String(10))
    code = Column(String(4))
    message = Column(String(100))
    request_date = Column(String(14))
    send_status = Column(String(20))

    payment = relationship("Payment", back_populates="sms_detail")


class PaymentLinkRequest(Base, TimestampMixin):
    __tablename__ = "payment_link_request"

    id = Column(Integer, primary_key=True)
    payment_id = Column(Integer, ForeignKey("payment.id"), unique=True)

    pg_tid = Column(String(100))
    pay_url = Column(String(200))
    expire_at = Column(DateTime)

    payment = relationship("Payment", back_populates="link_request")


class PaymentLinkResult(Base, TimestampMixin):
    __tablename__ = "payment_link_result"

    id = Column(Integer, primary_key=True)
    payment_id = Column(Integer, ForeignKey("payment.id"), unique=True)

    pg_tid = Column(String(100))
    pay_url = Column(String(200))
    expire_at = Column(DateTime)

    payment = relationship("Payment", back_populates="link_result")


class PaymentLinkCancel(Base, TimestampMixin):
    __tablename__ = "payment_link_cancel"

    id = Column(Integer, primary_key=True)
    payment_id = Column(Integer, ForeignKey("payment.id"), unique=True)

    pg_tid = Column(String(100))
    pay_url = Column(String(200))
    expire_at = Column(DateTime)

    payment = relationship("Payment", back_populates="link_cancel")


class PaymentLinkEnroll(Base, TimestampMixin):
    __tablename__ = "payment_link_enroll"

    id = Column(Integer, primary_key=True)
    payment_id = Column(Integer, ForeignKey("payment.id"), unique=True)

    pg_tid = Column(String(100))
    pay_url = Column(String(200))
    expire_at = Column(DateTime)

    payment = relationship("Payment", back_populates="link_enroll")


class PaymentManual(Base, TimestampMixin):
    __tablename__ = "payment_manual"

    id = Column(Integer, primary_key=True)
    payment_id = Column(Integer, ForeignKey("payment.id"), unique=True)

    amount = Column(Integer)
    card_number = Column(String(20))
    expire = Column(String(10))
    quota = Column(String(10))
    buyer_name = Column(String(50))
    goods_name = Column(String(100))
    phone = Column(String(50))

    tid = Column(String(50))
    code = Column(String(4))
    message = Column(String(100))
    app_number = Column(String(20))
    app_date = Column(String(10))
    van_cp_cd = Column(String(10))
    cp_cd = Column(String(10))
    van_iss_cp_cd = Column(String(10))
    iss_cp_cd = Column(String(10))

    payment = relationship("Payment", back_populates="manual_card_detail")


class PaymentCashReceipt(Base, TimestampMixin):
    __tablename__ = "payment_cash_receipt"

    id = Column(Integer, primary_key=True)
    payment_id = Column(Integer, ForeignKey("payment.id"), unique=True)
    cashbill_user_id = Column(Integer, ForeignKey("cashbill_users.id"), nullable=False)

    receipt_no = Column(String(100))
    receipt_type = Column(String(20))  # 소득공제 / 지출증빙
    approval_no = Column(String(20))

    payment = relationship("Payment", back_populates="cash_receipt_detail")
    cashbill_user = relationship("CashBillUser", back_populates="cash_receipt_detail")


class PaymentLog(Base, TimestampMixin):
    __tablename__ = "payment_log"

    id = Column(Integer, primary_key=True)
    payment_id = Column(Integer, ForeignKey("payment.id"), index=True)

    provider = Column(String(50))
    action = Column(String(50))

    request_data = Column(JSON)
    response_data = Column(JSON)

    status = Column(String(20))

    payment = relationship("Payment", back_populates="logs")


class CashBillUser(Base, TimestampMixin):
    __tablename__ = "cashbill_users"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    pobbill_user_id = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)

    user = relationship("User", back_populates="cashbill_user")
    cash_receipt_detail = relationship("PaymentCashReceipt", back_populates="cashbill_user",uselist=False)
