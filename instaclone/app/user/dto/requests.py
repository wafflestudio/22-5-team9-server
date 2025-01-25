from typing import Annotated, Optional, Callable, TypeVar
from pydantic import AfterValidator, BaseModel, EmailStr, HttpUrl
from instaclone.common.utils import validate_phone_number
from datetime import datetime, date, timedelta
from sqlalchemy import Date
import re
from functools import wraps
from enum import Enum


from instaclone.common.errors import InvalidFieldFormatError


T = TypeVar("T")
def skip_none(validator: Callable[[T], T]) -> Callable[[T | None], T | None]:
    @wraps(validator)
    def wrapper(value: T | None) -> T | None:
        if value is None:
            return value
        return validator(value)

    return wrapper

USERNAME_REGEX = re.compile(r"^(?![0-9]+$)(?!.*\.\.)[a-z0-9_.]+(?<!\.)$")

def validate_username(username: str) -> str:
    username = username.lower()
    if len(username) < 1 or len(username) > 30:
        raise InvalidFieldFormatError("Username must be between 1~30 characters.")
    if not USERNAME_REGEX.match(username):
        raise InvalidFieldFormatError("Username must only contain letters, numbers, '_', '.'\nPeriods must not come at end of usernames and consecutive periods are not permitted.\nUsername consisting of only numbers is not permitted.")
    
    return username

def validate_full_name(full_name: str) -> str:
    full_name = re.sub(r'\s+', ' ', full_name.strip())
    
    if not re.match(r'^[a-zA-Z]+(?: [a-zA-Z]+)*$', full_name):  # Korean name?
        raise InvalidFieldFormatError("Full name must contain only alphabetic characters and spaces.")
    
    return full_name

def validate_profile_image(profile_image: HttpUrl) -> HttpUrl:
    valid_extensions = (".jpg", ".jpeg", ".png", ".gif")
    pfp_str = str(profile_image)
    if not pfp_str.lower().endswith(valid_extensions):
        raise InvalidFieldFormatError("Profile image must be a URL to a valid image file (.jpg, .png, .gif, etc.).")
    return profile_image

def validate_description(description: str) -> str:
    if len(description) <= 100:
        return description
    else:
        raise InvalidFieldFormatError(f"{len(description)}/100 chars")

WEBSITE_REGEX = re.compile(
    r"^(https?:\/\/)?(www\.)?[a-zA-Z0-9-]{1,63}\.[a-zA-Z]{2,6}(\.[a-zA-Z]{2,6})?([\/\w.-]*)*\/?$"
)

def validate_website(url: str) -> str:
    if not WEBSITE_REGEX.match(url):
        raise InvalidFieldFormatError("Invalid website URL.")
    return url

def validate_password(password: str) -> str:
    if len(password) >= 6:
        return password
    else:
        raise InvalidFieldFormatError(f"Password is too short.")
    

class GenderEnum(str, Enum):
    MALE = "Male"
    Female = "Female"
    Other = "Other"
    Unknown = None

class UserEditRequest(BaseModel):
    username: Annotated[Optional[str], AfterValidator(skip_none(validate_username))] = None
    full_name: Annotated[Optional[str], AfterValidator(skip_none(validate_full_name))] = None
    introduce: Annotated[Optional[str], AfterValidator(skip_none(validate_description))] = None
    website: Annotated[Optional[str], AfterValidator(skip_none(validate_website))] = None
    gender: Annotated[Optional[GenderEnum], None] = None

class UserSigninRequest(BaseModel):
    username: str
    password: str

class UserSignupRequest(BaseModel):
    username: Annotated[str, AfterValidator(skip_none(validate_username))]
    password: Annotated[str, AfterValidator(skip_none(validate_password))]
    full_name: Annotated[str, AfterValidator(skip_none(validate_full_name))]
    email: EmailStr
    phone_number: Annotated[str, AfterValidator(skip_none(validate_phone_number))]
    birthday: Optional[date] = None
    gender: Optional[str] = None
    profile_image: Annotated[Optional[str], AfterValidator(skip_none(validate_profile_image))] = None
    introduce: Annotated[Optional[str], AfterValidator(skip_none(validate_description))] = None
    website: Annotated[Optional[str], AfterValidator(skip_none(validate_website))] = None