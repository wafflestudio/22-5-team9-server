from typing import Annotated
from fastapi import APIRouter, Depends

from instaclone.app.user.models import User
from instaclone.app.user.service import UserService
from instaclone.app.user.errors import InvalidTokenError
from instaclone.app.user.views import login_with_header

from instaclone.app.follower.dto.responses import FollowerDetailResponse, FollowerListResponse, FollowingListResponse
from instaclone.app.follower.dto.requests import FollowRequest
from instaclone.app.follower.service import FollowService

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

follower_router = APIRouter()
security = HTTPBearer()


@follower_router.get("/follower_number", status_code=HTTP_200_OK)
async def followers(user: User = Depends(login_with_header)) -> FollowerDetailResponse:
    return await FollowerDetailResponse.get_follower_number(user)

@follower_router.get("/followers", status_code=HTTP_200_OK)
async def get_followers(
    follower_service: FollowService = Depends(),
    user: User = Depends(login_with_header),
) -> FollowerListResponse:
    follower_ids = await follower_service.get_follower_list(user=user)
    return FollowerListResponse.from_follower_list(follower_ids)

@follower_router.get("/following", status_code=HTTP_200_OK)
async def get_following(
    follower_service: FollowService = Depends(),
    user: User = Depends(login_with_header),
) -> FollowingListResponse:
    following_ids = await follower_service.get_following_list(user=user)
    return FollowingListResponse.from_following_list(following_ids)

@follower_router.post("/follow", status_code=HTTP_201_CREATED)
async def follow(
    follower_service: FollowService = Depends(),
    follow_request: FollowRequest = Depends(),
    user: User = Depends(login_with_header)
) -> str:
    await follower_service.follow(
        user=user, 
        follow_id=follow_request.follow_id)
    return "SUCCESS"

@follower_router.post("/unfollow", status_code=HTTP_200_OK)
async def unfollow(
    follower_service: FollowService = Depends(),
    follow_request: FollowRequest = Depends(),
    user: User = Depends(login_with_header),
) -> str:
    await follower_service.unfollow(
        user=user,
        follow_id=follow_request.follow_id
    )
    return "SUCCESS"

