from abc import ABC, abstractmethod
from popbill import CashbillService, Cashbill, PopbillException, base
from fastapi import HTTPException
from app.core.config import settings
from app.domains.payment.schemas import CashBillUserRequest


class CashReceiptProviderInterface(ABC):
    @abstractmethod
    def check_member(self, business_number: str) -> dict:
        raise NotImplementedError()

    def company_info(self, business_number: str) -> dict:
        raise NotImplementedError()

    def join_member(self, data: CashBillUserRequest) -> dict:
        raise NotImplementedError()


class CashReceiptProvider(CashReceiptProviderInterface):
    cashbillService = CashbillService(settings.LinkID, settings.SecretKey)
    cashbillService.IsTest = settings.IsTest
    cashbillService.IPRestrictOnOff = settings.IPRestrictOnOff
    cashbillService.UseStaticIP = settings.UseStaticIP
    cashbillService.UseLocalTimeYN = settings.UseLocalTimeYN

    def check_member(self, business_number: str) -> dict:
        try:
            corp_num = business_number

            response = self.cashbillService.checkIsMember(corp_num)

            return {
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

    def company_info(self, business_number: str) -> dict:
        try:
            corp_num = business_number

            response = self.cashbillService.getCorpInfo(corp_num)

            return {
                "ceo": response.ceoname,
                "company_name": response.corpName,
                "address": response.addr,
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

    def join_member(self, data: CashBillUserRequest) -> dict:
        try:
            response = self.cashbillService.joinMember(data)

            return {
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
