class PaymentStateMachine:

    VALID_TRANSITIONS = {
        "INIT": ["PENDING", "ERROR"],
        "PENDING": ["SUCCESS", "FAIL", "ERROR", "EXPIRED"],
        "SUCCESS": ["CANCELED"],
        "FAIL": [],
        "ERROR": [],
        "EXPIRED": [],
        "CANCELED": [],
    }

    @classmethod
    def can_transition(cls, current: str, new: str) -> bool:
        return new in cls.VALID_TRANSITIONS.get(current, [])

    @classmethod
    def assert_transition(cls, current: str, new: str):
        if not cls.can_transition(current, new):
            raise ValueError(f"Invalid state transition: {current} → {new}")
