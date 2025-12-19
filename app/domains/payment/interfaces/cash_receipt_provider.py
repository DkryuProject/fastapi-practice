import asyncio
from abc import ABC, abstractmethod
from typing import ClassVar
from popbill import CashbillService, Cashbill, PopbillException
from fastapi import HTTPException
from app.core.config import settings


class CashReceiptProviderInterface(ABC):
    @abstractmethod
    async def check_member(self, business_number: str) -> dict:
        raise NotImplementedError()

    @abstractmethod
    async def issue(self, order_number: str, amount: int, identity: str) -> dict:
        raise NotImplementedError()
    
class CashReceiptProvider(CashReceiptProviderInterface):
    cashbillService: ClassVar[CashbillService] = CashbillService(
        settings.LinkID,
        settings.SecretKey
    )

    cashbillService.IsTest = settings.IsTest
    cashbillService.IPRestrictOnOff = settings.IPRestrictOnOff
    cashbillService.UseStaticIP = settings.UseStaticIP
    cashbillService.UseLocalTimeYN = settings.UseLocalTimeYN

    async def check_member(self, business_number: str) -> dict:
        try:
            corp_num = business_number

            response = await asyncio.to_thread(
                self.cashbillService.CheckIsMember ,
                corp_num
            )

            return  {
                "code": response.code,
                "message": response.message,
            }

        except PopbillException as e:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": e.code,
                    "message": e.message,
                }
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )


    async def issue(self, order_number: str, amount: int, identity: str) -> dict:
        try:
            corp_num = settings.POPBILL_CORP_NUM
            user_id = settings.POPBILL_USER_ID
            memo = "현금영수증 즉시 발행"

            cashbill = Cashbill(
                mgtKey=order_number,
                tradeDT=data.trade_dt,               # yyyyMMddHHmmss
                tradeType="승인거래",
                taxationType="과세",
                tradeOpt="일반",
                tradeUsage=data.receipt_type,         # 소득공제용 / 지출증빙용
                supplyCost=str(data.supply_cost),
                tax=str(data.tax),
                serviceFee="0",
                totalAmount=str(data.total_amount),
                franchiseCorpNum=corp_num,
                franchiseCorpName=data.franchise_name,
                franchiseCEOName=data.franchise_ceo,
                franchiseAddr=data.franchise_addr,
                franchiseTEL=data.franchise_tel,
                identityNum=data.identity,            # 휴대폰 / 사업자번호
                itemName=data.item_name,
                orderNumber=order_number,
                customerName=data.customer_name,
                email=data.email,
                hp=data.phone,
                smssendYN=False,
            )

            response = await asyncio.to_thread(
                self.cashbillService.registIssue,
                corp_num,
                cashbill,
                memo,
                user_id
            )

            return  {
                "code": response.code,
                "message": response.message,
            }

        except PopbillException as e:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": e.code,
                    "message": e.message,
                }
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=str(e)
            )
