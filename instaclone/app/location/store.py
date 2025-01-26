from instaclone.database.connection import SESSION
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.sql import exists, update
from datetime import datetime, timedelta

from instaclone.app.user.models import User
from instaclone.app.follower.models import Follower
from instaclone.app.location.models import LocationTag
from instaclone.app.location.errors import *

class LocationStore:
    async def add_location(self, name: str):
        existing_location_query = select(exists().where(LocationTag.name == name))
        existing_location = await SESSION.execute(existing_location_query)
        
        if existing_location.scalar():
            raise AlreadyExistLocationTagError()

        location = LocationTag(name=name)
        SESSION.add(location)
        try:
            await SESSION.commit()
        except IntegrityError:
            await SESSION.rollback()
            raise LocationCreationError()

    
    async def get_location_tags(self):
        current_time = datetime.utcnow()

        query = select(User.user_id, User.location_status).where(User.location_expired_at < current_time)
        result = await SESSION.execute(query)
        expired_users = result.all()

        for user_id, location_status in expired_users:
            current_location = await SESSION.scalar(select(LocationTag).where(LocationTag.location_id == location_status))
            if current_location:
                if location_status != 1:
                    current_location.citation_count = max(0, current_location.citation_count - 1)
                
                query = update(User).where(User.user_id == user_id).values(location_status=1, location_expired_at=current_time + timedelta(hours=100))
                await SESSION.execute(query)
                try:
                    await SESSION.commit()
                except IntegrityError:
                    await SESSION.rollback()
                    raise FetchError()
            else :
                raise LocationNotFoundError()

        query = select(LocationTag)
        result = await SESSION.execute(query)
        locations = result.scalars().all()

        sorted_locations = sorted(
            locations,
            key=lambda loc: loc.citation_count
        )
        return sorted_locations
    
    async def update_citation(self, old_tag_id: int, new_tag_id: int):
        if (old_tag_id == new_tag_id) :
            raise SameTagError()
        if (old_tag_id != 1) :
            old_location = await SESSION.scalar(select(LocationTag).where(LocationTag.location_id == old_tag_id))
            if old_location:
                old_location.citation_count = max(0, old_location.citation_count - 1)

        if (new_tag_id != 1) :
            new_location = await SESSION.scalar(select(LocationTag).where(LocationTag.location_id == new_tag_id))
            if new_location:
                new_location.citation_count += 1
        try:
            await SESSION.commit()
        except IntegrityError:
            await SESSION.rollback()
            raise FetchError()

    async def update_user_location_status(self, user_id: int, old_tag_id: int, new_tag_id: int, expire_at: datetime):
        if (old_tag_id == new_tag_id) :
            raise SameTagError()
        
        if (old_tag_id != 1) :
            old_location = await SESSION.scalar(select(LocationTag).where(LocationTag.location_id == old_tag_id))
            if old_location:
                old_location.citation_count = max(0, old_location.citation_count - 1)
            else :
                raise LocationNotFoundError()
        if (new_tag_id != 1) :
            new_location = await SESSION.scalar(select(LocationTag).where(LocationTag.location_id == new_tag_id))
            if new_location:
                new_location.citation_count += 1
            else :
                raise LocationNotFoundError()
        
        query = (
            update(User)
            .where(User.user_id == user_id)
            .values(location_status=new_tag_id, location_expired_at=expire_at)
        )
        await SESSION.execute(query)
        try:
            await SESSION.commit()
        except IntegrityError:
            await SESSION.rollback()
            raise FetchError()

    async def fetch_followers_by_location(self, user_id: int, location_id: int):
        location = await SESSION.scalar(select(LocationTag).where(LocationTag.location_id == location_id))
        if not location:
            raise LocationNotFoundError()
        query = (
            select(User.user_id)
            .join(Follower, Follower.follower_id == User.user_id)
            .where(
                Follower.following_id == user_id, 
                User.location_status == location_id,
                User.location_expired_at > datetime.utcnow()
            )
            .order_by(User.username)
        )

        result = await SESSION.execute(query)
        followers = [row[0] for row in result.all()]
        return followers