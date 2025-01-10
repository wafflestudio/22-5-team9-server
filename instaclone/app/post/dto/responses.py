from datetime import datetime
from pydantic import BaseModel
from typing import List
from instaclone.app.post.models import Post

class PostDetailResponse(BaseModel):
    post_id: int
    user_id: int
    location: str | None
    post_text: str | None
    creation_date: datetime
    file_url: List[str]

    @staticmethod
    def from_post(post: Post) -> "PostDetailResponse":
        file_urls = [m.url for m in post.media]
        return PostDetailResponse(
            post_id=post.post_id,
            user_id=post.user_id,
            location=post.location,
            post_text=post.post_text,
            creation_date=post.creation_date,
            file_url=file_urls
        )
