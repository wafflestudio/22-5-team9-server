from typing import List
from pydantic import BaseModel

from instaclone.app.comment.models import Comment
from instaclone.app.user.models import User
from instaclone.app.post.models import Post


class CommentDetailResponse(BaseModel):
    comment_id: int
    user_id: int
    post_id: int
    parent_id: int | None
    comment_text: str
    replies: List[int]

    @staticmethod
    async def from_comment(comment: Comment) -> "CommentDetailResponse":
        return CommentDetailResponse(
            comment_id=comment.comment_id,
            user_id=comment.user_id,
            post_id=comment.post_id,
            parent_id=comment.parent_id,
            comment_text=comment.comment_text,
            replies=[re.comment_id for re in comment.replies]
        )