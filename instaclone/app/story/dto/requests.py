from typing import List, Optional, Callable, TypeVar, Annotated
from pydantic import BaseModel, AfterValidator
from fastapi import UploadFile, File
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

def validate_cover_image(cover_image):
    print(type(cover_image))
    if type(cover_image) == str:
        if cover_image != "":
            raise InvalidFieldFormatError("Invalid image format")
    elif type(cover_image) != File:
        raise InvalidFieldFormatError("Invalid image format")
    else:
        valid_extensions = (".jpg", ".jpeg", ".png", ".gif")
        cimg_str = str(cover_image)
        if not cimg_str.lower().endswith(valid_extensions):
            raise InvalidFieldFormatError("Cover image must be a URL to a valid image file (.jpg, .png, .gif, etc.).")

    return cover_image

class StoryCreateRequest(BaseModel):
    media: List[UploadFile]

class StoryEditRequest(BaseModel):
    media: List[UploadFile]

class HighlightCreateRequest(BaseModel):
    highlight_name: Annotated[str, AfterValidator(validate_highlight_name)] = "Highlight"
    cover_image: Annotated[Optional[UploadFile] | str, AfterValidator(skip_none(validate_cover_image))] = None

class StorySaveHighlightRequest(BaseModel):
    highlight_id: int
    story_id: int
