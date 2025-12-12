from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.models_base import TimestampMixin


class Payment(Base, TimestampMixin):
    __tablename__ = "payment"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(30), unique=True, nullable=False, index=True)

    type = Column(String(20), nullable=False)  # sms, link, manual_card, cash_receipt
    amount = Column(Integer, nullable=False)
    status = Column(String(20))

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    sms_detail = relationship("PaymentSMS", back_populates="payment", uselist=False)
    link_detail = relationship("PaymentLink", back_populates="payment", uselist=False)
    manual_card_detail = relationship("PaymentManualCard", back_populates="payment", uselist=False)
    cash_receipt_detail = relationship("PaymentCashReceipt", back_populates="payment", uselist=False)

    logs = relationship("PaymentLog", back_populates="payment")
    user = relationship("User", back_populates="payment")

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


class PaymentLink(Base, TimestampMixin):
    __tablename__ = "payment_link"

    id = Column(Integer, primary_key=True)
    payment_id = Column(Integer, ForeignKey("payment.id"), unique=True)

    pg_tid = Column(String(100))
    pay_url = Column(String(200))
    expire_at = Column(DateTime)

    payment = relationship("Payment", back_populates="link_detail")


class PaymentManualCard(Base, TimestampMixin):
    __tablename__ = "payment_manual_card"

    id = Column(Integer, primary_key=True)
    payment_id = Column(Integer, ForeignKey("payment.id"), unique=True)

    card_bin = Column(String(10))
    card_last4 = Column(String(4))
    approval_no = Column(String(20))
    issuer = Column(String(50))

    payment = relationship("Payment", back_populates="manual_card_detail")


class PaymentCashReceipt(Base, TimestampMixin):
    __tablename__ = "payment_cash_receipt"

    id = Column(Integer, primary_key=True)
    payment_id = Column(Integer, ForeignKey("payment.id"), unique=True)

    receipt_no = Column(String(100))
    receipt_type = Column(String(20))  # 소득공제 / 지출증빙
    approval_no = Column(String(20))

    payment = relationship("Payment", back_populates="cash_receipt_detail")


class PaymentLog(Base, TimestampMixin):
    __tablename__ = "payment_log"

    id = Column(Integer, primary_key=True)
    payment_id = Column(Integer, ForeignKey("payment.id"), index=True)

    provider = Column(String(50))  # nicepay, sms_provider 등
    action = Column(String(50))    # request, callback, cancel 등

    request_data = Column(JSON)
    response_data = Column(JSON)

    status = Column(String(20))

    payment = relationship("Payment", back_populates="logs")
