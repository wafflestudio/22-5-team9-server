# from typing import Annotated
# from pydantic import AfterValidator, BaseModel

# from instaclone.common.errors import InvalidFieldFormatError

# # Validation definitions
# def validateComment(text: str | None) -> str | None:
#     return

# class CommentCreateRequest(BaseModel):
#     comment_text: Annotated[str, AfterValidator(validateComment)]
#     post_id: int
#     parent_id: int