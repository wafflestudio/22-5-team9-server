from typing import Annotated, List
from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from instaclone.app.comment.dto.requests import CommentCreateRequest, CommentEditRequest
from instaclone.app.comment.dto.responses import CommentDetailResponse, ReplyDetailResponse
from instaclone.app.comment.service import CommentService
from instaclone.app.post.service import PostService

from instaclone.app.user.models import User
from instaclone.app.user.views import login_with_header


comment_router = APIRouter()

@comment_router.post("/", status_code=HTTP_201_CREATED)
async def create_comment(
    user: Annotated[User, Depends(login_with_header)],
    comment_request: CommentCreateRequest,
    comment_service: Annotated[CommentService, Depends()],
    post_service: Annotated[PostService, Depends()]
) -> CommentDetailResponse:
    post = await post_service.get_post(comment_request.post_id)
    comment = await comment_service.create_comment(user=user, post=post, parent_id=comment_request.parent_id, comment_text=comment_request.comment_text)
    return CommentDetailResponse.from_comment(comment)

@comment_router.get("/{comment_id}", status_code=HTTP_200_OK)
async def get_comment_by_id(
    comment_id: int,
    comment_service: Annotated[CommentService, Depends()]
) -> CommentDetailResponse:
    comment = await comment_service.get_comment_by_id(comment_id)
    return CommentDetailResponse.from_comment(comment)

@comment_router.get("/{comment_id}/replies", status_code=HTTP_200_OK)
async def get_replies_from_comment(
    comment_id: int,
    comment_service: Annotated[CommentService, Depends()]
) -> List[ReplyDetailResponse]:
    replies = await comment_service.get_replies_from_comment(comment_id)
    return [ReplyDetailResponse.from_reply(r) for r in replies]

@comment_router.get("/list/{post_id}", status_code=HTTP_200_OK)
async def get_comment_by_post(
    post_id: int,
    comment_service: Annotated[CommentService, Depends()]
) -> List[CommentDetailResponse]:
    comments = await comment_service.get_comments_by_post(post_id)
    return [CommentDetailResponse.from_comment(c) for c in comments]

@comment_router.patch("/{comment_id}", status_code=HTTP_200_OK)
async def edit_comment(
    user: Annotated[User, Depends(login_with_header)],
    comment_id: int,
    comment_edit_request: CommentEditRequest,
    comment_service: Annotated[CommentService, Depends()]
) -> CommentDetailResponse:
    comment = await comment_service.edit_comment(user.user_id, comment_id, comment_edit_request.comment_text)
    return CommentDetailResponse.from_comment(comment)

@comment_router.delete("/{comment_id}", status_code=HTTP_200_OK)
async def delete_comment(
    user: Annotated[User, Depends(login_with_header)],
    comment_id: int,
    comment_service: Annotated[CommentService, Depends()]
) -> str:
    await comment_service.delete_comment(user.user_id, comment_id)
    return "SUCCESS"