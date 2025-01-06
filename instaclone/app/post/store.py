from typing import List
from instaclone.database.connection import SESSION
from sqlalchemy.sql import select

from instaclone.app.post.models import Post
from instaclone.database.annotation import transactional


class PostStore:
    async def get_post_by_id(self, post_id: int) -> Post | None:
        return await SESSION.scalar(select(Post).where(Post.post_id == post_id))
    
    async def get_posts_by_user(self, user_id: int) -> List[Post]:
        result = await SESSION.scalars(select(Post).where(Post.user_id == user_id))
        return result.all()
    
    @transactional
    async def add_post(self, user_id: int, location: str | None, post_text: str | None) -> Post:
        post = Post(user_id=user_id, location=location, post_text=post_text)
        SESSION.add(post)
        await SESSION.flush()
        return post

    @transactional
    async def delete_post(self, post_id: int) -> None:
        post = await self.get_post_by_id(post_id)
        if post:
            await SESSION.delete(post)
            await SESSION.flush()