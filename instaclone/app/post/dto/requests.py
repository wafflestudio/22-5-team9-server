from typing import Annotated, Optional, Callable, TypeVar, List
from pydantic import AfterValidator, BaseModel
from functools import wraps
from fastapi import UploadFile

from instaclone.common.errors import InvalidFieldFormatError


T = TypeVar("T")
def skip_none(validator: Callable[[T], T]) -> Callable[[T | None], T | None]:
    @wraps(validator)
    def wrapper(value: T | None) -> T | None:
        if value is None:
            return value
        return validator(value)

    return wrapper

def validate_location(location: str) -> str:
    if len(location) > 50:
        raise InvalidFieldFormatError(f"Location: {len(location)}/50 chars")
    
    return location

def validate_text(text: str) -> str:
    if len(text) > 500:
        raise InvalidFieldFormatError(f"Text: {len(text)}/500 chars")
    return text

class PostPutRequest(BaseModel):
    media: List[UploadFile]
    location: Annotated[str | None, AfterValidator(skip_none(validate_location))] = None
    post_text: Annotated[str | None, AfterValidator(skip_none(validate_text))] = None

class PostGetRequest(BaseModel):
    post_id: Optional[int] = None
    user_id: Optional[int] = None