from typing import List
from pydantic import BaseModel
from sqlalchemy.sql import select

from instaclone.app.comment.models import Comment
from instaclone.app.user.models import User
from instaclone.app.post.models import Post
from instaclone.database.annotation import SESSION

class CommentDetailResponse(BaseModel):
    comment_id: int
    user_id: int
    post_id: int
    parent_id: int | None
    comment_text: str

    @staticmethod
    def from_comment(comment: Comment) -> "CommentDetailResponse":
        return CommentDetailResponse(
            comment_id=comment.comment_id,
            user_id=comment.user_id,
            post_id=comment.post_id,
            parent_id=comment.parent_id,
            comment_text=comment.comment_text,
        )
    
class ReplyDetailResponse(BaseModel):
    comment_id: int
    user_id: int
    comment_text: str

    @staticmethod
    def from_reply(reply: Comment) -> "ReplyDetailResponse":
        return ReplyDetailResponse(
            comment_id=reply.comment_id,
            user_id=reply.user_id,
            comment_text=reply.comment_text
        )