from typing import Annotated, Sequence
from fastapi import Depends

from instaclone.app.comment.store import CommentStore
from instaclone.app.comment.models import Comment
from instaclone.app.comment.errors import CommentNotFoundError

class CommentService:
    def __init__(self, comments_store: Annotated[CommentStore, Depends()]):
        self.comments_store = comments_store

    async def create_comment(
        self,
        user_id: int,
        post_id: int,
        parent_id: int | None,
        comment_text: str,
    ) -> Comment:
        comment = await self.comments_store.create_comment(user_id=user_id, post_id=post_id, parent_id=parent_id, comment_text=comment_text)
        return comment
    
    async def get_comment_by_id(self, comment_id: int) -> Comment:
        comment = await self.comments_store.get_comment_by_id(comment_id)
        if not comment:
            raise CommentNotFoundError()
        return comment
    
    async def get_comments_by_post(self, post_id: int) -> Sequence[Comment]:
        comments = await self.comments_store.get_comments_by_post(post_id)
        return comments
    
    async def edit_comment(
        self,
        user_id: int,
        comment_id: int,
        comment_text: str
    ) -> Comment:
        comment = await self.comments_store.edit_comment(user_id, comment_id, comment_text)
        return comment

    async def delete_comment(self, user_id: int, comment_id: int) -> str:
        await self.comments_store.delete_comment(user_id, comment_id)
        return "SUCCESS"