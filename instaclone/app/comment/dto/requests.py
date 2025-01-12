from pydantic import BaseModel

class CommentCreateRequest(BaseModel):
    comment_text: str
    post_id: int
    parent_id: int | None = None

class CommentEditRequest(BaseModel):
    comment_text: str