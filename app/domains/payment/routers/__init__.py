from fastapi import APIRouter

# 개별 라우터 import
from .payment_router import router as payment_router
from .manual_payment_router import router as manual_router
from .sms_payment_router import router as sms_router
from .link_payment_router import router as link_router
from .cash_receipt_router import router as cash_router

# 통합 router 생성
router = APIRouter()

router.include_router(manual_router, prefix="/manual")            
router.include_router(sms_router, prefix="/sms")                  
router.include_router(link_router, prefix="/link")                
router.include_router(cash_router, prefix="/cash-receipt")
router.include_router(payment_router)    
      