import re


def validate_phone_with_plus(phone):
    res = re.fullmatch(r'\+\d{12}',phone)
    if not res:
        return False
    return True