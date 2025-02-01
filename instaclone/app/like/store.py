from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from instaclone.database.connection import SESSION
from instaclone.database.annotation import transactional
from instaclone.common.errors import InvalidFieldFormatError
from instaclone.app.user.models import User
from instaclone.app.story.models import Story
from instaclone.app.like.models import PostLike, StoryLike, CommentLike
from instaclone.app.like.errors import (
    AlreadyLikedError,
    LikeNotFoundError,
    LikeCreationError,
    ContentNotFoundError,
    SelfStoryLikeError
)

class LikeStore:
    @transactional
    async def add_like(self, user: User, content_id: int, like_type: str) -> object:
        # 각 좋아요 테이블을 get_like_table을 통해 선택
        table = self.get_like_table(like_type)  
        
        if like_type == 'story':
            story_query = await SESSION.execute(
                select(Story).where(Story.story_id == content_id)  # Story 테이블을 쿼리
            )
            story = story_query.scalars().first()

            if story is None:
                raise ContentNotFoundError()
            if story.user_id == user.user_id:
                raise SelfStoryLikeError()
            
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

        try:
            SESSION.add(new_like)
            await SESSION.commit()
        except IntegrityError:
            await SESSION.rollback()
            raise LikeCreationError()

        return new_like
    
    @transactional
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

        try:
            await SESSION.delete(like)
            await SESSION.commit()
        except IntegrityError:
            await SESSION.rollback()
            raise LikeCreationError()

    async def get_likers(self, content_id: int, like_type: str) -> list[int]:
        table = self.get_like_table(like_type)
        content_query = await SESSION.execute(
            select(table.content_id).where(table.content_id == content_id)
        )
        if not content_query.scalars().first():
            raise ContentNotFoundError()
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
            raise InvalidFieldFormatError("Choose 'post', 'story' or 'comment'")
