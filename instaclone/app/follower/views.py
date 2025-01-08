from typing import Annotated
from fastapi import APIRouter, Depends

from instaclone.app.user.models import User
from instaclone.app.user.service import UserService
from instaclone.app.user.errors import InvalidTokenError

from instaclone.app.follower.dto.responses import FollowerDetailResponse
from instaclone.app.follower.dto.requests import FollowRequest
from instaclone.app.follower.service import FollowService

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

follower_router = APIRouter()
security = HTTPBearer()


async def login_with_header(
    user_service: UserService = Depends(),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    token = credentials.credentials
    username = user_service.validate_access_token(token)
    user = await user_service.get_user_by_username(username)
    if not user:
        raise InvalidTokenError()
    return user


@follower_router.get("/follower_number", status_code=HTTP_200_OK)
async def followers(user: User = Depends(login_with_header)) -> FollowerDetailResponse:
    return await FollowerDetailResponse.get_follower_number(user)


@follower_router.post("/follow", status_code=HTTP_201_CREATED)
async def follow(follower_service: Annotated[FollowService, Depends()],
                 follow_request: FollowRequest,
                 user: User = Depends(login_with_header)
) -> str:
    await follower_service.follow(
        user=user, 
        follow_id=follow_request.follow_id)
    return "SUCCESS"