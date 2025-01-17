from typing import Annotated, List, Sequence
from fastapi import Depends

from instaclone.app.post.models import Post
from instaclone.app.post.store import PostStore
from instaclone.app.post.errors import PostNotFoundError
from instaclone.app.medium.models import Medium
from instaclone.app.user.models import User


class PostService:
    def __init__(self, post_store: Annotated[PostStore, Depends()]) -> None:
        self.post_store = post_store

    async def create_post(self, user: User, location: str | None, post_text: str | None, media: List[Medium]) -> Post:
        return await self.post_store.add_post(user=user, location=location, post_text=post_text, media=media)

    async def get_post(self, post_id: int) -> Post:
        post = await self.post_store.get_post_by_id(post_id)
        if not post:
            raise PostNotFoundError
        return post

    async def get_user_posts(self, user_id: int) -> Sequence[Post]:
        return await self.post_store.get_posts_by_user(user_id)

    async def delete_post(self, post_id: int) -> None:
        await self.post_store.delete_post(post_id)

    async def get_following_posts(self, follow_list: list[int]) -> list[Post]:
        posts = []
        for follow_id in follow_list:
            posts += await self.post_store.get_recent_posts_by_user(follow_id)
        sorted_posts: list[Post] = sorted(posts, key=lambda post: post.creation_date, reverse=True)

        return sorted_posts
    
    async def get_all_posts(self):
        return await self.post_store.get_all_posts()