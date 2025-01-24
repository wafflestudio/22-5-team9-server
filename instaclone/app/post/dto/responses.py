from datetime import datetime
from pydantic import BaseModel
from typing import List, Sequence
from sqlalchemy import select
from instaclone.app.post.models import Post
from instaclone.app.like.models import PostLike
from instaclone.app.comment.models import Comment
from instaclone.database.connection import SESSION

class PostDetailResponse(BaseModel):
    post_id: int
    user_id: int
    location: str | None
    post_text: str | None
    creation_date: datetime
    file_url: List[str]
    comments: Sequence[int]
    likes: Sequence[int]

    @staticmethod
    async def from_post(post: Post) -> "PostDetailResponse":
        file_urls = [m.url for m in post.media]

        comment_ids = await SESSION.execute(
            select(Comment.comment_id).where(Comment.post_id==post.post_id)
        )
        comment_ids = comment_ids.scalars().all()

        liker_ids = await SESSION.execute(
            select(PostLike.user_id).where(PostLike.content_id==post.post_id)
        )
        liker_ids = liker_ids.scalars().all()

        return PostDetailResponse(
            post_id=post.post_id,
            user_id=post.user_id,
            location=post.location,
            post_text=post.post_text,
            creation_date=post.creation_date,
            file_url=file_urls,
            comments=comment_ids,
            likes=liker_ids
        )
