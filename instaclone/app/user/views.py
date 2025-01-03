from typing import Annotated
from fastapi import APIRouter, Depends

from instaclone.app.user.dto.requests import UserEditRequest, UserSigninRequest, UserSignupRequest
from instaclone.app.user.dto.responses import UserDetailResponse, UserSigninResponse
from instaclone.app.user.service import UserService

from instaclone.app.user.models import User
from instaclone.app.user.service import UserService
from instaclone.app.user.dto.requests import UserEditRequest
from instaclone.app.user.errors import InvalidTokenError

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

user_router = APIRouter()

security = HTTPBearer()

async def login_with_header(
    user_service: Annotated[UserService, Depends()],
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> User:
    token = credentials.credentials
    username = user_service.validate_access_token(token)
    user = await user_service.get_user_by_username(username)
    if not user:
        raise InvalidTokenError()
    return user

@user_router.get("/profile", status_code=HTTP_200_OK)
async def me(user: Annotated[User, Depends(login_with_header)]) -> UserDetailResponse:
    return UserDetailResponse.from_user(user)

@user_router.patch("/profile/edit", status_code=HTTP_200_OK)
async def update_me(
    user: Annotated[User, Depends(login_with_header)],
    edit_request: UserEditRequest,
    user_service: Annotated[UserService, Depends()],
) -> UserDetailResponse:
    updated_user = await user_service.edit_user(
        user=user,
        username=edit_request.username,
        full_name=edit_request.full_name,
        introduce=edit_request.introduce,
        profile_image=edit_request.profile_image
    )
    return UserDetailResponse.from_user(updated_user)

@user_router.post("/signin", status_code=HTTP_200_OK)
async def signin(
    user_service: Annotated[UserService, Depends()],
    signin_request: UserSigninRequest
):
    access_token, refresh_token = await user_service.signin(signin_request.username, signin_request.password)
    
    return UserSigninResponse(access_token=access_token, refresh_token=refresh_token)

@user_router.post("/signup", status_code=HTTP_201_CREATED)
async def signup(
    user_service: Annotated[UserService, Depends()],
    signup_request: UserSignupRequest
):
    await user_service.signup(signup_request.username, signup_request.password, signup_request.full_name, signup_request.email, signup_request.phone_number)
    return "SUCCESS"