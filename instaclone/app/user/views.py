from typing import Annotated
from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK

from instaclone.app.user.service import UserService
from instaclone.app.user.dto.requests import UserSigninRequest
from instaclone.app.user.dto.responses import UserSigninResponse

user_router = APIRouter()

@user_router.post("/signin", status_code=HTTP_200_OK)
async def signin(
    user_service: Annotated[UserService, Depends()],
    signin_request: UserSigninRequest
):
    access_token, refresh_token = await user_service.signin(signin_request.username, signin_request.password)
    
    return UserSigninResponse(access_token=access_token, refresh_token=refresh_token)