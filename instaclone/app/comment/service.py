# from typing import Annotated
# from fastapi import Depends
# from instaclone.app.comment.dto.responses import CommentDetailResponse
# # from instaclone.app.comment.errors import
# from instaclone.app.comment.store import CommentStore
# from instaclone.app.post.errors import PostNotFoundError
# from instaclone.app.post.store import PostStore


# class CommentService:
#     def __init__(
#         self,
#         comments_store: CommentStore = Depends(),
#         post_store: PostStore = Depends()
#     ):
#         self.comments_store = comments_store
#         self.post_store = post_store
#         return

#     async def create_comment(
#         self,
#         user_id: int,
#         post_id: int,
#         parent_id: int | None,
#         comment_text: str,
#     ) -> CommentDetailResponse:
#         comment = await self.comments_store.create_comment(user_id=user_id, post_id=post_id, parent_id=parent_id, comment_text=comment_text)
#         return CommentDetailResponse.from_comment(comment)
    
#     async def list_coments(
#         self,
#         post_id : int | None = None,
#     ) -> list[CommentDetailResponse]:
#         if post_id is not None:
#             post = await self.post_store.get_post_by_id(post_id)
#             if post is None:
#                 raise PostNotFoundError()
#         comments = await self.comments_store.get_comments(post_id)
#         return [CommentDetailResponse.from_comment(comment) for comment in comments]