from .payment_router import router as payment_router
from .manual_payment_router import router as manual_router
from .sms_payment_router import router as sms_router
from .link_payment_router import router as link_router
from .cash_receipt_router import router as cash_router

payment_routers = [
    payment_router,
    manual_router,
    sms_router,
    link_router,
    cash_router
]
