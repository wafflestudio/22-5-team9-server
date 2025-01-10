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

post_router = APIRouter()

@post_router.post("/", status_code=HTTP_201_CREATED)
async def create_post(
    post_request: PostPutRequest,
    user: Annotated[User, Depends(login_with_header)],
    post_service: Annotated[PostService, Depends()],
) -> PostDetailResponse:
    post = await post_service.create_post(
        user_id=user.user_id,
        location=post_request.location,
        post_text=post_request.post_text,
    )
    return PostDetailResponse(
        post_id=post.post_id,
        user_id=post.user_id,
        location=post.location,
        post_text=post.post_text,
        creation_date=post.creation_date,
    )

@post_router.get("/{post_id}", status_code=HTTP_200_OK)
async def get_post(
    post_id: int,
    post_service: Annotated[PostService, Depends()],
) -> PostDetailResponse:
    post = await post_service.get_post(post_id)
    return PostDetailResponse(
        post_id=post.post_id,
        user_id=post.user_id,
        location=post.location,
        post_text=post.post_text,
        creation_date=post.creation_date,
    )

@post_router.get("/user/{username}", status_code=HTTP_200_OK)
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
        PostDetailResponse(
            post_id=post.post_id,
            user_id=post.user_id,
            location=post.location,
            post_text=post.post_text,
            creation_date=post.creation_date,
        )
        for post in posts
    ]

@post_router.get("/user/{user_id}", status_code=HTTP_200_OK)
async def get_user_posts_by_id(
    user_id: int,
    post_service: Annotated[PostService, Depends()],
) -> list[PostDetailResponse]:
    posts = await post_service.get_user_posts(user_id)
    return [
        PostDetailResponse(
            post_id=post.post_id,
            user_id=post.user_id,
            location=post.location,
            post_text=post.post_text,
            creation_date=post.creation_date,
        )
        for post in posts
    ]

@post_router.delete("/{post_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    post_service: Annotated[PostService, Depends()],
) -> None:
    await post_service.delete_post(post_id)
