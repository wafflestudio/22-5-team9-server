from typing import Annotated, List

from fastapi import Depends

from instaclone.app.user.models import User
from instaclone.app.like.store import LikeStore
from instaclone.app.like.models import PostLike, StoryLike, CommentLike

class LikeService:
    def __init__(self, like_store: Annotated[LikeStore, Depends()]) -> None:
        self.like_store = like_store

    async def like(self, user: User, content_id: int, like_type: str) -> object:
        return await self.like_store.add_like(user=user, content_id=content_id, like_type=like_type)

    async def unlike(self, user: User, content_id: int, like_type: str) -> None:
        return await self.like_store.remove_like(user=user, content_id=content_id, like_type=like_type)

    async def get_likers(self, content_id: int, like_type: str) -> List[int]:
        return await self.like_store.get_likers(content_id=content_id, like_type=like_type)