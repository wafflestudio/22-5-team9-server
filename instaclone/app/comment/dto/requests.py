from typing import TypeVar, Callable, Annotated, Optional
from pydantic import BaseModel, AfterValidator
from functools import wraps

from instaclone.app.comment.errors import CommentLengthLimitError

T = TypeVar("T")
def skip_none(validator: Callable[[T], T]) -> Callable[[T | None], T | None]:
    @wraps(validator)
    def wrapper(value: T | None) -> T | None:
        if value is None:
            return value
        return validator(value)

    return wrapper

def validate_comment_text(comment_text: str) -> str:
    if len(comment_text) > 200:
        raise CommentLengthLimitError()
    
    return comment_text

class CommentCreateRequest(BaseModel):
    comment_text: Annotated[str, AfterValidator(skip_none(validate_comment_text))]
    post_id: int
    parent_id: Optional[int] = None

class CommentEditRequest(BaseModel):
    comment_text: Annotated[str, AfterValidator(skip_none(validate_comment_text))]