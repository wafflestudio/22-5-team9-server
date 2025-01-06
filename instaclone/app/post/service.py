from typing import Annotated
from fastapi import Depends

from instaclone.app.post.models import Post
from instaclone.app.post.store import PostStore
from instaclone.app.post.errors import PostNotFoundError


class PostService:
    def __init__(self, post_store: Annotated[PostStore, Depends()]) -> None:
        self.post_store = post_store

    async def create_post(self, user_id: int, location: str | None, post_text: str | None) -> Post:
        return await self.post_store.add_post(user_id=user_id, location=location, post_text=post_text)

    async def get_post(self, post_id: int) -> Post:
        post = await self.post_store.get_post_by_id(post_id)
        if not post:
            raise PostNotFoundError
        return post

    async def get_user_posts(self, user_id: int) -> list[Post]:
        return await self.post_store.get_posts_by_user(user_id)

    async def delete_post(self, post_id: int) -> None:
        await self.post_store.delete_post(post_id)
