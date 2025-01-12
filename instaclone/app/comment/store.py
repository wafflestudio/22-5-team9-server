from typing import Sequence
from sqlalchemy.sql import select, delete

from instaclone.app.user.models import User
from instaclone.app.post.models import Post
from instaclone.app.comment.models import Comment
from instaclone.app.comment.errors import CommentNotFoundError, CommentPermissionError
from instaclone.database.connection import SESSION

class CommentStore:
    async def get_comment_by_id(self, comment_id: int) -> Comment | None:
        return await SESSION.scalar(select(Comment).where(Comment.comment_id == comment_id))
        
    async def create_comment(
        self, 
        user: User,
        post: Post,
        comment_text: str,
        parent_id: int | None = None
    ) -> Comment:
        if parent_id:
            parent_comment = await self.get_comment_by_id(parent_id)
        else:
            parent_comment = None
        comment = Comment(user=user, post=post, parent=parent_comment, comment_text=comment_text)
        SESSION.add(comment)
        await SESSION.commit()
        return comment
    
    async def get_comments_by_post(self, post_id: int) -> Sequence["Comment"]:
        query = select(Comment).where(Comment.post_id == post_id)

        result = await SESSION.scalars(query)
        comments = result.all()

        return comments
    
    async def get_replies_from_comment(self, comment_id: int) -> Sequence["Comment"]:
        query = select(Comment).where(Comment.parent_id == comment_id)

        result = await SESSION.scalars(query)
        replies = result.all()
        
        return replies
    
    async def edit_comment(self, user_id: int, comment_id: int, comment_text: str) -> Comment:
        comment = await SESSION.scalar(select(Comment).where(Comment.comment_id == comment_id))
        
        if not comment:
            raise CommentNotFoundError()
        if comment.user_id != user_id:
            raise CommentPermissionError()
        
        comment.comment_text = comment_text
        await SESSION.commit()
        return comment
    
    async def delete_comment(self, user_id: int, comment_id: int) -> str:
        query = select(Comment).where(Comment.comment_id == comment_id)
        comment = await SESSION.scalar(query)

        if not comment:
            raise CommentNotFoundError()
        if comment.user_id != user_id:
            raise CommentPermissionError()
        
        delete_query = delete(Comment).where(Comment.comment_id == comment_id)
        await SESSION.execute(delete_query)
        await SESSION.commit()
        return "SUCCESS"