from fastapi import Depends
from typing import Annotated
from datetime import datetime, timedelta

from instaclone.common.errors import InvalidFieldFormatError
from instaclone.app.location.store import LocationStore
from instaclone.app.location.dto.responses import LocationResponse


class LocationService:
    def __init__(self, location_store: Annotated[LocationStore, Depends()]):
        self.location_store = location_store

    async def create_location(self, name: str):
        await self.location_store.add_location(name)

    async def get_all_locations(self):
        locations = await self.location_store.get_location_tags()
        return [
            LocationResponse(
                tag_id=loc.location_id,
                name=loc.name,
                citation=loc.citation_count
            )
            for loc in locations
        ]

    async def update_location_status(self, user_id: int, old_tag_id: int, new_tag_id: int, expiration_delta: int, expiration_unit: str):
        if expiration_delta <= 0:
            raise InvalidFieldFormatError("Expiration delta must be positive")

        if expiration_unit == "hours":
            delta = timedelta(hours=expiration_delta)
        elif expiration_unit == "days":
            delta = timedelta(days=expiration_delta)
        elif expiration_unit == "minutes":
            delta = timedelta(minutes=expiration_delta)
        else:
            raise InvalidFieldFormatError("Invalid expiration unit")

        current_time = datetime.utcnow()
        expiration_time = current_time + delta

        await self.location_store.update_user_location_status(user_id, old_tag_id, new_tag_id, expiration_time)


    async def get_followers_by_location(self, user_id: int, location_id: int):
        return await self.location_store.fetch_followers_by_location(user_id, location_id)
        