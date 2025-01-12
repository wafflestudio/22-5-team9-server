from typing import Sequence
from sqlalchemy.sql import select, delete

from instaclone.app.user.models import User
from instaclone.app.post.models import Post
from instaclone.app.comment.models import Comment
from instaclone.app.comment.errors import CommentNotFoundError, CommentPermissionError, CommentServerError
from instaclone.app.post.errors import PostNotFoundError
from instaclone.database.connection import SESSION

class CommentStore:
    async def get_comment_by_id(self, comment_id: int) -> Comment:
        comment = await SESSION.scalar(select(Comment).where(Comment.comment_id == comment_id))
        if not comment:
            raise CommentNotFoundError()
        return comment
        
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
        try:
            SESSION.add(comment)
            await SESSION.commit()
            return comment
        
        except Exception as e:
            await SESSION.rollback()
            raise CommentServerError() from e
    
    async def get_comments_by_post(self, post_id: int) -> Sequence["Comment"]:
        post = await SESSION.scalar(select(Post).where(Post.post_id == post_id))
        if not post:
            raise PostNotFoundError()

        query = select(Comment).where(Comment.post_id == post_id)

        result = await SESSION.scalars(query)
        comments = result.all()

        return comments
    
    async def get_replies_from_comment(self, comment_id: int) -> Sequence["Comment"]:
        await self.get_comment_by_id(comment_id)

        query = select(Comment).where(Comment.parent_id == comment_id)

        result = await SESSION.scalars(query)
        replies = result.all()
        
        return replies
    
    async def edit_comment(self, user_id: int, comment_id: int, comment_text: str) -> Comment:
        comment = await self.get_comment_by_id(comment_id)
        if comment.user_id != user_id:
            raise CommentPermissionError()
        
        comment.comment_text = comment_text
        try:
            await SESSION.commit()
            return comment
        
        except Exception as e:
            await SESSION.rollback()
            raise CommentServerError() from e
    
    async def delete_comment(self, user_id: int, comment_id: int) -> str:
        comment = await self.get_comment_by_id(comment_id)

        if comment.user_id != user_id:
            raise CommentPermissionError()
        child_delete_query = delete(Comment).where(Comment.parent_id == comment_id)
        delete_query = delete(Comment).where(Comment.comment_id == comment_id)
        await SESSION.execute(child_delete_query)
        await SESSION.execute(delete_query)
        try:
            await SESSION.commit()
            return "SUCCESS"
        
        except Exception as e:
            await SESSION.rollback()
            raise CommentServerError() from e