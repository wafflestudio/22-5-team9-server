from datetime import datetime
from sqlalchemy.exc import IntegrityError
from instaclone.app.user.models import User
from instaclone.app.follower.models import Follower
from instaclone.database.connection import SESSION
from instaclone.database.annotation import transactional
from instaclone.app.follower.errors import AlreadyFollowingError, FollowCreationError, UserNotFoundError

class FollowerStore:
    @transactional
    async def add_follow(self, user: User, follow_id: int) -> Follower:
        follow_user = await SESSION.get(User, follow_id)
        if not follow_user:
            raise UserNotFoundError()

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
        