from typing import Annotated
from fastapi import APIRouter, Depends, Query

from instaclone.app.user.views import login_with_header
from instaclone.app.user.models import User
from instaclone.app.location.service import LocationService
from instaclone.app.location.dto.requests import LocationRequest
from instaclone.app.location.dto.responses import LocationResponse
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

location_router = APIRouter()

@location_router.post("/", status_code=HTTP_201_CREATED)
async def add_tag(
    user: Annotated[User, Depends(login_with_header)],
    location_service: Annotated[LocationService, Depends()],
    name: str
) -> str:
    await location_service.create_location(user.user_id, name=name)
    return "SUCCESS"

@location_router.get("/my", status_code=HTTP_200_OK)
async def get_my_tag(
    user: Annotated[User, Depends(login_with_header)],
    location_service: Annotated[LocationService, Depends()]
) -> int:
    return await location_service.get_location(user.user_id)

@location_router.get("/{tag_id}", status_code=HTTP_200_OK)
async def get_tag_by_id(
    tag_id: int,
    location_service: Annotated[LocationService, Depends()] 
) -> LocationResponse :
    return await location_service.get_tag(tag_id)

@location_router.get("/loc_tags", status_code=HTTP_200_OK)
async def get_all_tags(
    location_service: Annotated[LocationService, Depends()],
) -> list[LocationResponse]:
    return await location_service.get_all_locations()

@location_router.post("/status", status_code=HTTP_200_OK)
async def assign_locate_status(
    user: Annotated[User, Depends(login_with_header)],
    location_service: Annotated[LocationService, Depends()],
    location_request: LocationRequest = Depends(),
):
    await location_service.update_location_status(user.user_id, user.location_status, location_request.tag_id, location_request.expiration_delta, location_request.expiration_unit)
    return "SUCCESS"

@location_router.get("/world", status_code=HTTP_200_OK)
async def get_followers_with_same_location(
    user: Annotated[User, Depends(login_with_header)],
    location_service: Annotated[LocationService, Depends()],
    location_id: int
) -> list[int]:
    return await location_service.get_followers_by_location(user.user_id, location_id)

@location_router.get("/search", status_code=HTTP_200_OK)
async def search_by_location_name(
    location_service: Annotated[LocationService, Depends()],
    name: str
) -> list[int]:
    return await location_service.get_locations_matching_name(name)
    

@location_router.delete("/{tag_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_location_tag(
    tag_id: int,
    user: Annotated[User, Depends(login_with_header)],
    location_service: Annotated[LocationService, Depends()]
) -> None:
    await location_service.delete_tag(tag_id, user.user_id)