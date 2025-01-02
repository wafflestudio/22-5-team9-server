from typing import Optional
from instaclone.common.errors import InvalidFieldFormatError

import re

EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
PHONE_NUMBER_PATTERN = re.compile(r'^010\d{8}$')
USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9._]{3,30}$')

def validate_phone_number(value: str | None) -> str | None:
    if value is None:
        return None
    if not value.startswith("010") or not len(value) == 11 or not value.isdigit():
        raise InvalidFieldFormatError()
    return value

def identify_input_type(input_str: str) -> Optional[str]:
    """
    주어진 문자열이 email, phone_number, username중 어떤 것인지 확인하고 반환합니다.
    """

    if EMAIL_PATTERN.match(input_str):
        return "email"
    elif PHONE_NUMBER_PATTERN.match(input_str):
        return "phone_number"
    elif USERNAME_PATTERN.match(input_str):
        return "username"
    else:
        return None