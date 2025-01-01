from pydantic import EmailStr, ValidationError
from typing import Optional

import re

EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
PHONE_NUMBER_PATTERN = r'^010\d{8}$'
USERNAME_PATTERN = r'^[a-zA-Z0-9._]{3,30}$'

def identify_input_type(input_str: str) -> Optional[str]:
    """
    주어진 문자열이 email, phone_number, username중 어떤 것인지 확인하고 반환합니다.
    """

    if re.match(EMAIL_PATTERN, input_str):
        return "email"
    elif re.match(PHONE_NUMBER_PATTERN, input_str):
        return "phone_number"
    elif re.match(USERNAME_PATTERN, input_str):
        return "username"
    else:
        return None

