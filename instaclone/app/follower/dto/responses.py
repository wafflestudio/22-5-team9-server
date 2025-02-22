from typing import List
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.future import select
from instaclone.database.connection import SESSION
from instaclone.database.annotation import transactional
from instaclone.app.user.models import User
from instaclone.app.follower.models import Follower


class FollowerDetailResponse(BaseModel):
    follower_count: int
    following_count: int

    @staticmethod
    # @transactional
    async def get_follower_number(user: User) -> "FollowerDetailResponse":
        follower_result = await SESSION.execute(
            select(func.count(Follower.follower_id)).where(Follower.following_id == user.user_id)
        )
        follower_count = follower_result.scalar()

        following_result = await SESSION.execute(
            select(func.count(Follower.follower_id)).where(Follower.follower_id == user.user_id)
        )
        following_count = following_result.scalar()

        return FollowerDetailResponse(
            follower_count=follower_count,
            following_count=following_count
        )

class FollowerListResponse(BaseModel):
    follower_ids: List[int]
    @staticmethod
    def from_follower_list(follower_ids: List[int]) -> "FollowerListResponse":
        return FollowerListResponse(follower_ids=follower_ids)
    
    @staticmethod
    async def get_followers(user: User) -> list[int]:
        query = select(Follower.follower_id).where(Follower.following_id == user.user_id)
        result = await SESSION.execute(query)
        follower_ids = [row[0] for row in result.fetchall()]
        return follower_ids
        
    
class FollowingListResponse(BaseModel):
    following_ids: List[int]
    @staticmethod
    def from_following_list(following_ids: List[int]) -> "FollowingListResponse":
        return FollowingListResponse(following_ids=following_ids)
    
    @staticmethod
    async def get_following(user: User) -> list[int]:
        query = select(Follower.following_id).where(Follower.follower_id == user.user_id)
        result = await SESSION.execute(query)
        following_ids = [row[0] for row in result.fetchall()]
        return following_ids