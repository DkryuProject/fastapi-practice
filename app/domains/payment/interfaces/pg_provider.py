from abc import ABC, abstractmethod


class PGProviderInterface(ABC):
    @abstractmethod
    def create_payment_link(self, amount: int, product_name: str, order_number: str) -> dict:
        raise NotImplementedError()


class DummyPGProvider(PGProviderInterface):
    def create_payment_link(self, amount: int, product_name: str, order_number: str) -> dict:
        return {
            "pay_url": f"https://pay.example.com/{order_number}",
            "tid": "TID" + order_number[-6:],
            "status": "ready",
        }
