from typing import Annotated
from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from instaclone.app.post.dto.requests import PostPutRequest, PostGetRequest
from instaclone.app.post.dto.responses import PostDetailResponse
from instaclone.app.post.service import PostService
from instaclone.app.user.models import User
from instaclone.app.user.views import login_with_header
from instaclone.app.user.service import UserService
from instaclone.app.user.errors import UserDoesNotExistError
from instaclone.app.medium.service import MediumService

post_router = APIRouter()

@post_router.post("/", status_code=HTTP_201_CREATED)
async def create_post(
    user: Annotated[User, Depends(login_with_header)],
    post_service: Annotated[PostService, Depends()],
    medium_service: Annotated[MediumService, Depends()],
    post_request: PostPutRequest = Depends()
) -> PostDetailResponse:
    media = [await medium_service.file_to_medium(file) for file in post_request.media]
    post = await post_service.create_post(
        user=user,
        location=post_request.location,
        post_text=post_request.post_text,
        media=media
    )
    return PostDetailResponse.from_post(post)

@post_router.get("/{post_id}", status_code=HTTP_200_OK)
async def get_post(
    post_id: int,
    post_service: Annotated[PostService, Depends()],
) -> PostDetailResponse:
    post = await post_service.get_post(post_id)
    return PostDetailResponse.from_post(post)



@post_router.get("/user/{user_parameter}", status_code=HTTP_200_OK)
async def get_user_posts(
    user_parameter,
    post_service: Annotated[PostService, Depends()],
    user_service: Annotated[UserService, Depends()]
):
    try:
        user_parameter = int(user_parameter)
        return await get_user_posts_by_id(user_id=user_parameter, post_service=post_service)
    except ValueError:
        return await get_user_posts_by_username(username=str(user_parameter), user_service=user_service, post_service=post_service)
    
async def get_user_posts_by_id(
    user_id: int,
    post_service: Annotated[PostService, Depends()],
) -> list[PostDetailResponse]:
    posts = await post_service.get_user_posts(user_id)
    return [
        PostDetailResponse.from_post(post)
        for post in posts
    ]

# @post_router.get("/user/{username}", status_code=HTTP_200_OK)
async def get_user_posts_by_username(
    username: str,
    user_service: Annotated[UserService, Depends()],
    post_service: Annotated[PostService, Depends()],
) -> list[PostDetailResponse]:
    user = await user_service.get_user_by_username(username)
    if user == None:
        raise UserDoesNotExistError
    posts = await post_service.get_user_posts(user.user_id)
    return [
        PostDetailResponse.from_post(post)
        for post in posts
    ]

@post_router.delete("/{post_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    post_service: Annotated[PostService, Depends()],
) -> None:
    await post_service.delete_post(post_id)
