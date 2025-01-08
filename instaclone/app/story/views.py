from typing import Annotated, List
from fastapi import APIRouter, Depends, UploadFile, File
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from instaclone.app.user.views import login_with_header
from instaclone.app.user.models import User
from instaclone.app.story.dto.requests import StoryCreateRequest, StoryEditRequest
from instaclone.app.story.dto.responses import StoryDetailResponse
from instaclone.app.story.models import Story
from instaclone.app.story.service import StoryService
from instaclone.app.medium.models import Medium

story_router = APIRouter()

@story_router.post("/", status_code=HTTP_201_CREATED)
async def create_story(
    user: Annotated[User, Depends(login_with_header)],
    # story_create_request: StoryCreateRequest,
    files: List[UploadFile],
    story_service: Annotated[StoryService, Depends()]
) -> StoryDetailResponse:
    # List[UploadFile] -> List[Medium]
    media = [await story_service.file_to_medium(file) for file in files]
    story = await story_service.create_story(user, media)
    return StoryDetailResponse.from_story(story)

@story_router.get("/{story_id}", status_code=HTTP_200_OK)
async def get_story(
    story_id: int,
    story_service: Annotated[StoryService, Depends()]
) -> StoryDetailResponse:
    story = await story_service.get_story(story_id)
    return StoryDetailResponse.from_story(story)

@story_router.get("/list/{user_id}", status_code=HTTP_200_OK)
async def get_stories(
    user_id: int,
    story_service: Annotated[StoryService, Depends()]
) -> List[StoryDetailResponse]:
    story_list = await story_service.get_story_list(user_id)
    return [StoryDetailResponse.from_story(story) for story in story_list]

@story_router.post("/edit/{story_id}", status_code=HTTP_200_OK)
async def edit_story(
    user: Annotated[User, Depends(login_with_header)],
    # story_edit_request: StoryEditRequest,
    files: List[UploadFile],
    story_id: int,
    story_service: Annotated[StoryService, Depends()]
) -> StoryDetailResponse:
    # List[UploadFile] -> List[Medium]
    media = [await story_service.file_to_medium(file) for file in files]
    story = await story_service.edit_story(user, story_id, media)
    return StoryDetailResponse.from_story(story)

@story_router.delete("/{story_id}", status_code=HTTP_200_OK)
async def delete_story(
    user: Annotated[User, Depends(login_with_header)],
    story_id: int,
    story_service: Annotated[StoryService, Depends()]
) -> str:
    await story_service.delete_story(user, story_id)
    return "SUCCESS"