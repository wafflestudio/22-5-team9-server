from typing import List, Sequence
from instaclone.database.connection import SESSION
from sqlalchemy.sql import select, desc

from instaclone.app.post.models import Post
from instaclone.database.annotation import transactional
from instaclone.app.medium.models import Medium
from instaclone.app.user.models import User
from instaclone.app.comment.models import Comment
from datetime import datetime, timezone
from instaclone.app.post.errors import PostEditPermissionError, PostNotFoundError, PostSaveFailedError, PostDeleteFailedError, PostDeletePermissionError


class PostStore:
    async def get_post_by_id(self, post_id: int) -> Post | None:
        return await SESSION.scalar(select(Post).where(Post.post_id == post_id))
    
    async def get_posts_by_user(self, user_id: int) -> Sequence[Post]:
        result = await SESSION.scalars(select(Post).where(Post.user_id == user_id))
        return result.all()
    
    async def get_recent_posts_by_user(self, user_id: int) -> Sequence[Post]:
        result = await SESSION.scalars(select(Post).where(Post.user_id == user_id).order_by(desc(Post.creation_date)).limit(2))
        return result.all()
    @transactional
    async def add_post(self, user: User, location: str | None, post_text: str | None, media: List[Medium]) -> Post:
        post = Post(user_id=user.user_id, location=location, post_text=post_text, media=media, creation_date=datetime.now(timezone.utc), user=user)
        try:
            SESSION.add(post)
            await SESSION.commit()
            return post
        except:
            await SESSION.rollback()
            raise PostSaveFailedError()

    @transactional
    async def delete_post(self, post_id: int) -> None:
        post = await self.get_post_by_id(post_id)
        comments = await SESSION.execute(
            select(Comment).where(Comment.post_id==post_id)
        )
        comments = comments.scalars().all()

        try:
            if comments:
                for comment in comments:
                    await SESSION.delete(comment)
            if post:
                await SESSION.delete(post)
                await SESSION.commit()
                # await SESSION.flush()
        except:
            await SESSION.rollback()
            raise PostDeleteFailedError()

    @transactional
    async def update_post(
        self,
        post_id: int,
        location: str | None,
        post_text: str | None
    ) -> Post | None:
        post = await self.get_post_by_id(post_id)
        if not post:
            raise PostNotFoundError()
        try:
            if location is not None:
                post.location = location
            if post_text is not None:
                post.post_text = post_text
            await SESSION.commit()
            return post
        except:
            await SESSION.rollback()
            raise PostSaveFailedError()
      
    async def get_all_posts(self):
        posts = await SESSION.execute(
            select(Post).order_by(desc(Post.creation_date))
        )
        return posts.scalars().all()
