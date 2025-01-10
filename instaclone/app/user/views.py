from typing import Annotated
from fastapi import APIRouter, Depends

from instaclone.app.user.dto.requests import UserEditRequest, UserSigninRequest, UserSignupRequest, GenderEnum
from instaclone.app.user.dto.responses import UserDetailResponse, UserSigninResponse, RefreshTokenResponse
from instaclone.app.user.service import UserService

from instaclone.app.user.models import User
from instaclone.app.user.service import UserService
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
    return await UserDetailResponse.from_user(user)

@user_router.patch("/profile/edit", status_code=HTTP_200_OK)
async def update_me(
    user: Annotated[User, Depends(login_with_header)],
    user_service: Annotated[UserService, Depends()],
    edit_request: UserEditRequest = Depends(),
) -> UserDetailResponse:
    updated_user = await user_service.edit_user(
        user=user,
        username=edit_request.username,
        full_name=edit_request.full_name,
        introduce=edit_request.introduce,
        profile_image=edit_request.profile_image,
        website=edit_request.website,
        gender=edit_request.gender
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
) -> str:
    await user_service.signup(
        signup_request.username, 
        signup_request.password, 
        signup_request.full_name, 
        signup_request.email, 
        signup_request.phone_number, 
        signup_request.gender, 
        signup_request.birthday, 
        signup_request.profile_image, 
        signup_request.introduce,
        signup_request.website
    )
    return "SUCCESS"

@user_router.post("/refresh", status_code=HTTP_200_OK)
async def refresh_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_service: Annotated[UserService, Depends()]
) -> RefreshTokenResponse:
    refresh_token = credentials.credentials
    new_access_token, new_refresh_token = await user_service.refresh_token(refresh_token)
    return RefreshTokenResponse(access_token=new_access_token, refresh_token=new_refresh_token)