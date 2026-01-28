import re


def normalize_card_number(text: str) -> str:
    text = text.upper()

    replace_map = {
        "O": "0",
        "I": "1",
        "L": "1",
        "S": "5",
        "B": "8"
    }

    for k, v in replace_map.items():
        text = text.replace(k, v)

    return re.sub(r"[^0-9]", "", text)


def luhn_check(card_number: str) -> bool:
    if not card_number.isdigit():
        return False

    total = 0
    reverse = card_number[::-1]

    for i, ch in enumerate(reverse):
        n = int(ch)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n

    return total % 10 == 0
