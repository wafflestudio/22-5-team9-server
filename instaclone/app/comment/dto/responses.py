from typing import Self
from pydantic import BaseModel

from instaclone.app.comment.models import Comment
from instaclone.app.user.models import User
from instaclone.app.post.models import Post


class CommentDetailResponse(BaseModel):
    comment_id: int
    user: User
    post: Post
    parent: Comment | None
    comment_text: str
    replies: list["Comment"]

    @staticmethod
    def from_comment(comment: Comment) -> "CommentDetailResponse":
        return CommentDetailResponse(
            comment_id=comment.comment_id,
            user=comment.user,
            post=comment.post,
            parent=comment.parent,
            comment_text=comment.comment_text,
            replies=comment.replies
        )