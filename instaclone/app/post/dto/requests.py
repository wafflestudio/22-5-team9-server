from typing import Annotated, Optional, Callable, TypeVar
from pydantic import AfterValidator, BaseModel
from functools import wraps


from instaclone.common.errors import InvalidFieldFormatError


T = TypeVar("T")
def skip_none(validator: Callable[[T], T]) -> Callable[[T | None], T | None]:
    @wraps(validator)
    def wrapper(value: T | None) -> T | None:
        if value is None:
            return value
        return validator(value)

    return wrapper

def validate_address(address: str) -> str:
    if len(address) > 50:
        raise InvalidFieldFormatError(f"Address: {len(address)}/50 chars")
    
    return address

def validate_text(text: str) -> str:
    if len(text) > 500:
        raise InvalidFieldFormatError(f"Text: {len(text)}/500 chars")
    return text

class PostRequest(BaseModel):
    user_id: Annotated[int, None]
    location: Annotated[Optional[str], AfterValidator(skip_none(validate_address))]
    post_text: Annotated[Optional[str], AfterValidator(skip_none(validate_text))]