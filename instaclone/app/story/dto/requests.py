from typing import List, Optional, Callable, TypeVar, Annotated
from pydantic import BaseModel, AfterValidator
from fastapi import UploadFile
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

def validate_highlight_name(name):
    try:
        name = int(name)
        raise InvalidFieldFormatError("Highlight names must include characters that are not numbers")
    except ValueError:
        if not isinstance(name, str):
            raise InvalidFieldFormatError("Name must be string")
        if len(name) > 15:
            raise InvalidFieldFormatError(f"Too long: {len(name)}/15")
    return name

class StoryCreateRequest(BaseModel):
    media: List[UploadFile]

class StoryEditRequest(BaseModel):
    media: List[UploadFile]

class HighlightCreateRequest(BaseModel):
    highlight_name: Annotated[str, AfterValidator(validate_highlight_name)] = "Highlight"
    cover_image: Optional[UploadFile] = None

class StorySaveHighlightRequest(BaseModel):
    highlight_id: int
    story_id: int
