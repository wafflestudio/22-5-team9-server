from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from instaclone.database.connection import SESSION
from instaclone.app.user.models import User
from instaclone.app.like.models import PostLike, StoryLike, CommentLike
from instaclone.app.like.errors import (
    AlreadyLikedError,
    LikeNotFoundError,
    LikeCreationError,
)

class LikeStore:
    async def add_like(self, user: User, content_id: int, like_type: str) -> object:
        # 각 좋아요 테이블을 get_like_table을 통해 선택
        table = self.get_like_table(like_type)  
        existing_like = await SESSION.execute(
            select(table).where(
                table.user_id == user.user_id,
                table.content_id == content_id,
            )
        )
        if existing_like.scalars().first():
            raise AlreadyLikedError()

        # 새로운 좋아요 추가
        new_like = table(
            user_id=user.user_id,
            content_id=content_id,
        )

        SESSION.add(new_like)
        try:
            await SESSION.commit()
        except IntegrityError:
            await SESSION.rollback()
            raise LikeCreationError()

        return new_like
        
    async def remove_like(self, user: User, content_id: int, like_type: str) -> None:
        table = self.get_like_table(like_type)
        existing_like = await SESSION.execute(
            select(table).where(
                table.user_id == user.user_id,
                table.content_id == content_id,
            )
        )
        like = existing_like.scalars().first()
        if not like:
            raise LikeNotFoundError()

        await SESSION.delete(like)
        try:
            await SESSION.commit()
        except IntegrityError:
            await SESSION.rollback()
            raise LikeCreationError()

    async def get_likers(self, content_id: int, like_type: str) -> list[int]:
        table = self.get_like_table(like_type)
        result = await SESSION.execute(
            select(table.user_id).where(
                table.content_id == content_id,
            )
        )
        return [row[0] for row in result.fetchall()]
    

    def get_like_table(self, like_type: str):
        if like_type == 'post':
            return PostLike
        elif like_type == 'story':
            return StoryLike
        elif like_type == 'comment':
            return CommentLike
        else:
            raise ValueError("Invalid like type")
