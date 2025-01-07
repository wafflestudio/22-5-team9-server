from typing import List, Sequence
from datetime import datetime, timezone
from sqlalchemy.sql import select, delete

from instaclone.app.user.models import User
from instaclone.app.medium.models import Medium
from instaclone.app.story.models import Story
from instaclone.database.annotation import transactional
from instaclone.database.connection import SESSION
from instaclone.app.story.errors import StoryNotExistsError, StoryPermissionError, UserNotFoundError

class StoryStore:
    async def get_user_from_id(self, user_id: int) -> User:
        user = await SESSION.scalar(select(User).where(User.user_id == user_id))
        if not user:
            raise UserNotFoundError()
        return user

    @transactional
    async def add_story(
        self, 
        user: User,
        media: List["Medium"]
    ) -> Story:
        story = Story(user=user, media=media, creation_date=datetime.now(timezone.utc))
        SESSION.add(story)
        return story
    
    async def get_story_list(
        self,
        user: User
    ) -> Sequence["Story"]:
        query = select(Story).where(
            Story.user_id == user.user_id,
            Story.expiration_date < datetime.now(timezone.utc)
        ).order_by(Story.creation_date)

        result = await SESSION.scalars(query)
        stories = result.all()

        return stories
    
    async def get_story(
        self,
        story_id: int
    ) -> Story:
        query = select(Story).where(Story.story_id == story_id)
        story = await SESSION.scalar(query)

        if not story:
            raise StoryNotExistsError()

        return story
    
    @transactional
    async def edit_story(
        self,
        user: User,
        media: List["Medium"],
        story_id: int
    ) -> Story:
        query = select(Story).where(Story.story_id == story_id)
        story = await SESSION.scalar(query)

        if not story:
            raise StoryNotExistsError()
        if story.user_id != user.user_id:
            raise StoryPermissionError()
        
        story.media = media
        await SESSION.flush()
        return story

    @transactional
    async def delete_story(
        self,
        user: User,
        story_id: int
    ) -> str:
        query = select(Story).where(Story.story_id == story_id)
        story = await SESSION.scalar(query)

        if not story:
            raise StoryNotExistsError()
        if story.user_id != user.user_id:
            raise StoryPermissionError()
        
        delete_query = delete(Story).where(Story.story_id == story_id)
        await SESSION.execute(delete_query)

        return "SUCCESS"
        