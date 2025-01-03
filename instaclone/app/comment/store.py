# from typing import Sequence
# from sqlalchemy.sql import select
# from sqlalchemy.orm import joinedload

# from instaclone.app.comment.models import Comment
# from instaclone.app.post.models import Post
# from instaclone.database.annotation import transactional
# from instaclone.database.connection import SESSION


# class CommentStore:
#     @transactional
#     async def create_comment(
#         self, 
#         user_id: int,
#         post_id: int,
#         comment_text: str,
#         parent_id: int | None = None
#     ) -> Comment:
#         comment = Comment(user_id=user_id, post_id=post_id, parent_id=parent_id, comment_text=comment_text)
#         SESSION.add(comment)
#         await SESSION.flush()
#         return comment

#     async def get_comment_by_id(self, comment_id: int) -> Comment | None:
#         comment = await SESSION.get(Comment, comment_id)
#         return comment

#     async def get_comments(
#         self,
#         post_id: int | None = None
#     ) -> Sequence[Comment]:
#         comments_list_query = select(Comment).options(joinedload((Comment.post)))
#         if post_id is not None:
#             comments_list_query = comments_list_query.where(Comment.post_id == post_id)
#         return (await SESSION.scalars(comments_list_query)).all()