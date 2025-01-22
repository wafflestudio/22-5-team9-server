from typing import Annotated, List
from fastapi import APIRouter, Depends, UploadFile, File
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from pydantic import BaseModel
from starlette import datastructures

from instaclone.app.user.views import login_with_header
from instaclone.app.user.models import User
from instaclone.app.story.dto.requests import StoryCreateRequest, StoryEditRequest, HighlightCreateRequest, StorySaveHighlightRequest
from instaclone.app.story.dto.responses import StoryDetailResponse, HighlightDetailResponse
from instaclone.app.story.models import Story
from instaclone.app.story.service import StoryService
from instaclone.app.medium.models import Medium
from instaclone.app.medium.service import MediumService

story_router = APIRouter()

@story_router.post("/", status_code=HTTP_201_CREATED)
async def create_story(
    user: Annotated[User, Depends(login_with_header)],
    # story_create_request: StoryCreateRequest,
    files: List[UploadFile],
    story_service: Annotated[StoryService, Depends()],
    medium_service: Annotated[MediumService, Depends()]
) -> StoryDetailResponse:
    # List[UploadFile] -> List[Medium]
    media = [await medium_service.file_to_medium(file) for file in files]
    story = await story_service.create_story(user, media)
    return StoryDetailResponse.from_story(story)

@story_router.get("/{story_id}", status_code=HTTP_200_OK)
async def get_story(
    story_id: int,
    user: Annotated[User, Depends(login_with_header)],  
    story_service: Annotated[StoryService, Depends()]
) -> StoryDetailResponse:
    story = await story_service.get_story(story_id, user)
    return StoryDetailResponse.from_story(story)

@story_router.get("/list/{user_id}", status_code=HTTP_200_OK)
async def get_stories(
    user_id: int,
    story_service: Annotated[StoryService, Depends()]
) -> List[StoryDetailResponse]:
    story_list = await story_service.get_story_list(user_id)
    return [StoryDetailResponse.from_story(story) for story in story_list]

@story_router.patch("/edit/{story_id}", status_code=HTTP_200_OK)
async def edit_story(
    user: Annotated[User, Depends(login_with_header)],
    # story_edit_request: StoryEditRequest,
    files: List[UploadFile],
    story_id: int,
    story_service: Annotated[StoryService, Depends()],
    medium_service: Annotated[MediumService, Depends()]
) -> StoryDetailResponse:
    # List[UploadFile] -> List[Medium]
    media = [await medium_service.file_to_medium(file) for file in files]
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


######## Highlight views #######

# Create highlight and add new story
@story_router.post("/highlight/new/{story_id}", status_code=HTTP_201_CREATED)
async def add_new_highlight(
    user: Annotated[User, Depends(login_with_header)],
    story_id: int,
    story_service: Annotated[StoryService, Depends()],
    medium_service: Annotated[MediumService, Depends()],
    highlight_create_request: HighlightCreateRequest = Depends(),
) -> HighlightDetailResponse:
    if type(highlight_create_request.cover_image) == datastructures.UploadFile:
        cover_image = await medium_service.create_medium(highlight_create_request.cover_image)
    else:
        story = await story_service.get_story_no_validation(story_id=story_id, current_user=user)
        cover_image = story.media[0]
    highlight = await story_service.create_highlight(user=user, highlight_cover=cover_image, highlight_name=highlight_create_request.highlight_name)
    highlight = await story_service.add_init_user_highlight(user=user, highlight=highlight)
    highlight = await story_service.add_story_highlight(user=user, story_id=story_id, highlight_id=highlight.highlight_id)
    response = await HighlightDetailResponse.from_highlight(highlight=highlight)
    return response

# # Add story to existing highlight
@story_router.post("/highlight/add/{highlight_id}/{story_id}", status_code=HTTP_201_CREATED)
async def add_to_highlight(
    user: Annotated[User, Depends(login_with_header)],
    highlight_id: int,
    story_id: int,
    story_service: Annotated[StoryService, Depends()]
):
    highlight = await story_service.add_story_highlight(user=user, story_id=story_id, highlight_id=highlight_id)
    return await HighlightDetailResponse.from_highlight(highlight=highlight)

@story_router.post("/highlight/add_user/{highlight_id}/{user_id}", status_code=HTTP_201_CREATED)
async def add_user_to_highlight(
    user: Annotated[User, Depends(login_with_header)],
    highlight_id: int,
    user_id: int,
    story_service: Annotated[StoryService, Depends()]
):
    highlight = await story_service.add_user_highlight(user=user, user_id=user_id, highlight_id=highlight_id)
    return await HighlightDetailResponse.from_highlight(highlight=highlight)

# # Get all highlights of a user using user id
@story_router.get("/highlights/{user_id}", status_code=HTTP_200_OK)
async def get_highlights(
    user_id: int,
    story_service: Annotated[StoryService, Depends()],
    ) ->  List[HighlightDetailResponse]:
    highlights = await story_service.get_highlight_list(user_id=user_id)
    return [await HighlightDetailResponse.from_highlight(highlight) for highlight in highlights]

# # Get single highlight using highlight_id
@story_router.get("/highlight/{highlight_id}", status_code=HTTP_200_OK)
async def get_highlight(
    highlight_id: int,
    story_service: Annotated[StoryService, Depends()]
) -> HighlightDetailResponse:
    return await HighlightDetailResponse.from_highlight(await story_service.get_highlight(highlight_id=highlight_id))

@story_router.delete("/highlight/{highlight_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_highlight(
    user: Annotated[User, Depends(login_with_header)],
    highlight_id: int,
    story_service: Annotated[StoryService, Depends()]
):
    await story_service.delete_highlight(user=user, highlight_id=highlight_id)
    return "Success"

@story_router.delete("/highlightstory/{highlight_id}/{story_id}")
async def unsave_story(
    user: Annotated[User, Depends(login_with_header)],
    highlight_id: int,
    story_id: int,
    story_service: Annotated[StoryService, Depends()]
):
    await story_service.unsave_story(user=user, highlight_id=highlight_id, story_id=story_id)
    return "Success"

@story_router.delete("/highlightuser/{highlight_id}/{user_id}")
async def remove_user_from_highlight(
    user: Annotated[User, Depends(login_with_header)],
    highlight_id: int,
    user_id: int,
    story_service: Annotated[StoryService, Depends()]
):
    await story_service.remove_highlight_user(user=user, highlight_id=highlight_id, user_id=user_id)
    return "Success"

@story_router.patch("/highlight/change_admin/{user_id}", status_code=HTTP_200_OK)
async def change_highlight_admin(
    user: Annotated[User, Depends(login_with_header)],
    highlight_id: int,
    user_id: int,
    story_service: Annotated[StoryService, Depends()]
):
    highlight = await story_service.change_highlight_admin(user=user, highlight_id=highlight_id, user_id=user_id)
    return await HighlightDetailResponse.from_highlight(highlight)

class StoryViewerResponse(BaseModel):
    user_id: int
    username: str

    @staticmethod
    def from_user(user: User) -> "StoryViewerResponse":
        return StoryViewerResponse(
            user_id=user.user_id,
            username=user.username
        )

@story_router.get("/{story_id}/viewers", status_code=HTTP_200_OK)
async def get_story_viewers(
    story_id: int,
    owner: Annotated[User, Depends(login_with_header)],   # story owner
    story_service: Annotated[StoryService, Depends()]
) -> List[StoryViewerResponse]:
    viewers = await story_service.get_story_viewers(story_id, owner)
    return [StoryViewerResponse.from_user(v) for v in viewers] # returning list of viewers that viewed the story

