from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, UploadFile, Form
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from instaclone.app.post.dto.requests import PostPutRequest, PostGetRequest, PostPatchRequest
from instaclone.app.post.dto.responses import PostDetailResponse
from instaclone.app.post.service import PostService
from instaclone.app.user.models import User
from instaclone.app.user.views import login_with_header
from instaclone.app.user.service import UserService
from instaclone.app.follower.service import FollowService
from instaclone.app.user.errors import UserDoesNotExistError
from instaclone.app.medium.service import MediumService

post_router = APIRouter()

@post_router.post("/", status_code=HTTP_201_CREATED)
async def create_post(
    user: Annotated[User, Depends(login_with_header)],
    post_service: Annotated[PostService, Depends()],
    medium_service: Annotated[MediumService, Depends()],
    media: List[UploadFile],
    post_text: Optional[str] = Form(None),
    location: Optional[str] = Form(None)
) -> PostDetailResponse:
    post_request = PostPutRequest(
        media=media,
        location=location,
        post_text=post_text
    )
    post_media = [await medium_service.file_to_medium(file) for file in post_request.media]
    post = await post_service.create_post(
        user=user,
        location=post_request.location,
        post_text=post_request.post_text,
        media=post_media
    )
    return await PostDetailResponse.from_post(post)

@post_router.get("/explore", status_code=HTTP_200_OK)
async def explore_tab(
    post_service: Annotated[PostService, Depends()]
):
    posts = await post_service.get_all_posts()
    return [
        await PostDetailResponse.from_post(post)
        for post in posts
    ]

@post_router.get("/{post_id}", status_code=HTTP_200_OK)
async def get_post(
    post_id: int,
    post_service: Annotated[PostService, Depends()],
) -> PostDetailResponse:
    post = await post_service.get_post(post_id)
    return await PostDetailResponse.from_post(post)



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

@post_router.get("/posts/following")
async def get_following_posts(
    user: Annotated[User, Depends(login_with_header)],
    post_service: Annotated[PostService, Depends()],
    follow_service: Annotated[FollowService, Depends()]        
) -> list[PostDetailResponse]:
    follow_list = await follow_service.get_following_list(user)
    posts = await post_service.get_following_posts(follow_list=follow_list)
    return [
        await PostDetailResponse.from_post(post)
        for post in posts
    ]

async def get_user_posts_by_id(
    user_id: int,
    post_service: Annotated[PostService, Depends()],
) -> list[PostDetailResponse]:
    posts = await post_service.get_user_posts(user_id)
    return [
        await PostDetailResponse.from_post(post)
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
        await PostDetailResponse.from_post(post)
        for post in posts
    ]


@post_router.delete("/{post_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    user: Annotated[User, Depends(login_with_header)],
    post_service: Annotated[PostService, Depends()],
) -> None:
    await post_service.delete_post(post_id, user)

@post_router.patch("/{post_id}", status_code=HTTP_200_OK)
async def edit_post(
    post_id: int,
    user: Annotated[User, Depends(login_with_header)],
    post_service: Annotated[PostService, Depends()],
    location: Optional[str] = Form(None),
    post_text: Optional[str] = Form(None)
) -> PostDetailResponse:
    post_request = PostPatchRequest(
        location=location,
        post_text=post_text
    )
    updated_post = await post_service.edit_post(
        post_id=post_id,
        current_user=user,
        location=post_request.location,
        post_text=post_request.post_text
    )
    return await PostDetailResponse.from_post(updated_post)
