from abc import ABC, abstractmethod


class CashReceiptProviderInterface(ABC):
    @abstractmethod
    def issue(self, amount: int, receipt_type: str, identity: str) -> dict:
        raise NotImplementedError()


class DummyCashReceiptProvider(CashReceiptProviderInterface):
    def issue(self, amount: int, receipt_type: str, identity: str) -> dict:
        return {
            "receipt_no": "RC" + identity[-4:],
            "approval_no": "APR" + identity[-4:],
            "status": "issued",
        }
