# from typing import Self
# from pydantic import BaseModel

# from instaclone.app.comment.models import Comment
# from instaclone.app.user.models import User
# from instaclone.app.post.models import Post


# class CommentDetailResponse(BaseModel):
#     comment_id: int
#     user_id: int
#     post_id: int
#     parent: int | None
#     comment_text: str
#     replies: list[int]

#     @staticmethod
#     def from_comment(comment: Comment) -> "CommentDetailResponse":
#         if comment.parent:
#             parent = comment.parent
#             parent_id = parent.comment_id
#         else:
#             parent_id = None
#         reply_ids = []
#         if comment.replies:
#             for reply in comment.replies:
#                 reply_ids.append(reply.comment_id)

#         return CommentDetailResponse(
#             comment_id=comment.comment_id,
#             user_id=comment.user_id,
#             post_id=comment.post_id,
#             parent=parent_id,
#             comment_text=comment.comment_text,
#             replies=reply_ids
#         )