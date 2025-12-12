from abc import ABC, abstractmethod


class ManualCardProviderInterface(ABC):
    @abstractmethod
    def approve(self, card_number: str, expiry: str, cvc: str, amount: int) -> dict:
        raise NotImplementedError()


class DummyManualProvider(ManualCardProviderInterface):
    def approve(self, card_number: str, expiry: str, cvc: str, amount: int) -> dict:
        return {
            "approval_no": "APP" + card_number[-4:],
            "issuer": "dummy_bank",
            "status": "approved",
            "last4": card_number[-4:],
        }
