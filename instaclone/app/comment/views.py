# from typing import Annotated
# from fastapi import APIRouter, Depends

# from instaclone.app.comment.dto.requests import CommentCreateRequest
# from instaclone.app.comment.dto.responses import CommentDetailResponse
# from instaclone.app.comment.service import CommentService

# from instaclone.app.user.models import User
# from instaclone.app.user.views import login_with_header


# comment_router = APIRouter()


# @comment_router.post("", status_code=201)
# async def create_comment(
#     user: Annotated[User, Depends(login_with_header)],
#     comment: CommentCreateRequest,
#     comment_service: Annotated[CommentService, Depends()],
# ) -> CommentDetailResponse:
#     return await comment_service.create_comment(user_id=user.user_id, post_id=comment.post_id, parent_id=comment.parent_id, comment_text=comment.comment_text)


# @comment_router.get("", status_code=200)
# async def get_comments(
#     comment_service: Annotated[CommentService, Depends()],
#     post_id: int | None
# ) -> list[CommentDetailResponse]:
#     return await comment_service.list_coments(post_id)