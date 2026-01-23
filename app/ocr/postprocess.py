import re

def luhn(card_number: str) -> bool:
    total = 0
    reverse = card_number[::-1]

    for i, d in enumerate(reverse):
        n = int(d)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n

    return total % 10 == 0

def issuer(card_number):
    if card_number.startswith("4"):
        return "VISA"
    if card_number[:2] in ["34", "37"]:
        return "AMEX"
    if card_number[:2] in [str(i) for i in range(51, 56)]:
        return "MASTERCARD"
    return "UNKNOWN"

def parse_card_number(text: str):
    digits = re.sub(r"\D", "", text)

    if len(digits) < 13 or len(digits) > 19:
        return None

    if not luhn(digits):
        return None

    return {
        "card_number": digits,
        "issuer": issuer(digits),
        "masked": f"{digits[:4]}********{digits[-4:]}"
    }
