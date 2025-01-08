from typing import Annotated

from fastapi import Depends

from instaclone.app.follower.store import FollowerStore
from instaclone.app.follower.models import Follower
from instaclone.app.user.models import User


class FollowService:
    def __init__(self, follower_store: Annotated[FollowerStore, Depends()]) -> None:
        self.follower_store = follower_store

    async def follow(self, user: User, follow_id: int) -> Follower:
        return await self.follower_store.add_follow(user=user, follow_id=follow_id)