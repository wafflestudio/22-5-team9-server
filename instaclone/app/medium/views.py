from typing import Annotated, List
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from instaclone.app.medium.dto.responses import MediumResponse
from instaclone.app.medium.service import MediumService

medium_router = APIRouter()

'''@medium_router.post("/", status_code=HTTP_201_CREATED)
async def upload_medium(
    medium_service: Annotated[MediumService, Depends()],
    post_id: int = Form(None),
    #story_id: int = Form(None),
    file: UploadFile = File(...),
) -> MediumResponse:
    try:
        medium = await medium_service.create_medium(post_id=post_id, 
                                                    #story_id=story_id, 
                                                    file=file)
        return MediumResponse(
            image_id=medium.image_id,
            post_id=medium.post_id,
            #story_id=medium.story_id,
            file_name=medium.file_name,
            url=medium.url,
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))'''

@medium_router.post("/", status_code=201)
async def upload_medium(
    medium_service: Annotated[MediumService, Depends()],
    post_id: int = Form(None),
    #story_id: int = Form(None),
    file: UploadFile = File(...)
) -> MediumResponse:
    """
    Upload a medium file and save it locally.
    """
    try:
        medium = await medium_service.create_medium(post_id=post_id, 
                                                    #story_id=story_id, 
                                                    file=file)
        return MediumResponse(
            image_id=medium.image_id,
            post_id=medium.post_id,
            #story_id=medium.story_id,
            file_name=medium.file_name,
            url=medium.url,
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@medium_router.get("/{image_id}", status_code=HTTP_200_OK)
async def get_medium(
    image_id: int,
    medium_service: Annotated[MediumService, Depends()],
) -> MediumResponse:
    try:
        medium = await medium_service.get_medium(image_id)
        return MediumResponse(
            image_id=medium.image_id,
            post_id=medium.post_id,
            #story_id=medium.story_id,
            file_name=medium.file_name,
            url=medium.url,
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="Medium not found")

@medium_router.get("/post/{post_id}", status_code=HTTP_200_OK)
async def get_media_by_post(
    post_id: int,
    medium_service: Annotated[MediumService, Depends()],
) -> List[MediumResponse]:
    media = await medium_service.get_media_by_post(post_id)
    return [
        MediumResponse(
            image_id=medium.image_id,
            post_id=medium.post_id,
            #story_id=medium.story_id,
            file_name=medium.file_name,
            url=medium.url,
        )
        for medium in media
    ]

@medium_router.delete("/{image_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_medium(
    image_id: int,
    medium_service: Annotated[MediumService, Depends()],
) -> None:
    try:
        await medium_service.delete_medium(image_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Medium not found")