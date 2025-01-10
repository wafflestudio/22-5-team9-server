from typing import List
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from instaclone.app.user.models import User
from instaclone.app.follower.models import Follower
from instaclone.database.connection import SESSION
from instaclone.database.annotation import transactional
from instaclone.app.follower.errors import CannotFollowSelfError, AlreadyFollowingError, FollowCreationError, UserNotFoundError, NotFollowingError

class FollowerStore:
    @transactional
    async def add_follow(self, user: User, follow_id: int) -> Follower:
        follow_user = await SESSION.get(User, follow_id)
        if not follow_user:
            raise UserNotFoundError()
        
        if user.user_id == follow_id:
            raise CannotFollowSelfError()

        existing_follow = await SESSION.get(Follower, (user.user_id, follow_id))
        if existing_follow:
            raise AlreadyFollowingError()

        new_follow = Follower(
            follower_id=user.user_id,
            following_id=follow_id,
        )

        SESSION.add(new_follow)
        try:
            await SESSION.commit()
        except IntegrityError:
            await SESSION.rollback()
            raise FollowCreationError()

        return new_follow
        
    @transactional
    async def remove_follow(self, user: User, follow_id: int) -> None:
        existing_follow = await SESSION.get(Follower, (user.user_id, follow_id))
        if not existing_follow:
            raise NotFollowingError()
        
        await SESSION.delete(existing_follow)
        try:
            await SESSION.commit()
        except IntegrityError:
            await SESSION.rollback()
            raise FollowCreationError()
        
    @transactional
    async def get_followers(self, user: User) -> List[int]:
        query = select(Follower.follower_id).where(Follower.following_id == user.user_id)
        result = await SESSION.execute(query)
        follower_ids = [row[0] for row in result.fetchall()]
        return follower_ids
    
    @transactional
    async def get_following(self, user: User) -> List[int]:
        query = select(Follower.following_id).where(Follower.follower_id == user.user_id)
        result = await SESSION.execute(query)
        following_ids = [row[0] for row in result.fetchall()]
        return following_ids