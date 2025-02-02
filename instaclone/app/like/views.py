from typing import Annotated
from fastapi import APIRouter, Depends, Query

from instaclone.app.like.service import LikeService
from instaclone.app.like.dto.requests import LikeRequest
from instaclone.app.like.dto.responses import LikeResponse
from instaclone.app.user.views import login_with_header
from instaclone.app.user.models import User

from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

like_router = APIRouter()

@like_router.post("/post_like", status_code=HTTP_201_CREATED)
async def post_like(
    like_service: LikeService = Depends(),
    like_request: LikeRequest = Depends(),
    user: User = Depends(login_with_header),
) -> str:
    await like_service.like(
        user=user,
        content_id=like_request.content_id,
        like_type='post'
    )
    return "SUCCESS"

@like_router.post("/story_like", status_code=HTTP_201_CREATED)
async def story_like(
    like_service: LikeService = Depends(),
    like_request: LikeRequest = Depends(),
    user: User = Depends(login_with_header),
) -> str:
    await like_service.like(
        user=user,
        content_id=like_request.content_id,
        like_type='story'
    )
    return "SUCCESS"

@like_router.post("/comment_like", status_code=HTTP_201_CREATED)
async def comment_like(
    like_service: LikeService = Depends(),
    like_request: LikeRequest = Depends(),
    user: User = Depends(login_with_header),
) -> str:
    await like_service.like(
        user=user,
        content_id=like_request.content_id,
        like_type='comment'
    )
    return "SUCCESS"


@like_router.delete("/post_unlike", status_code=HTTP_204_NO_CONTENT)
async def post_unlike(
    like_service: LikeService = Depends(),
    like_request: LikeRequest = Depends(),
    user: User = Depends(login_with_header),
) -> None:
    await like_service.unlike(
        user=user,
        content_id=like_request.content_id,
        like_type='post'
    )

@like_router.delete("/story_unlike", status_code=HTTP_204_NO_CONTENT)
async def story_unlike(
    like_service: LikeService = Depends(),
    like_request: LikeRequest = Depends(),
    user: User = Depends(login_with_header),
) -> None:
    await like_service.unlike(
        user=user,
        content_id=like_request.content_id,
        like_type='story'
    )

@like_router.delete("/comment_unlike", status_code=HTTP_204_NO_CONTENT)
async def comment_unlike(
    like_service: LikeService = Depends(),
    like_request: LikeRequest = Depends(),
    user: User = Depends(login_with_header),
) -> None:
    await like_service.unlike(
        user=user,
        content_id=like_request.content_id,
        like_type='comment'
    )


@like_router.get("/likers", status_code=HTTP_200_OK)
async def get_likers(
    like_service: LikeService = Depends(),
    content_id: int = Query(..., description="The ID of the content to get likers for"),
    like_type: str = Query(..., description="The type of like to filter by"),
) -> LikeResponse:
    likers = await like_service.get_likers(content_id=content_id, like_type=like_type)
    return LikeResponse(liker_ids=likers, content_id=content_id, like_type=like_type)
