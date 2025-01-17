from typing import List, Sequence
from datetime import datetime, timezone
from sqlalchemy.sql import select, delete

from instaclone.app.user.models import User
from instaclone.app.medium.models import Medium
from instaclone.app.story.models import Story, StoryView
from instaclone.database.annotation import transactional
from instaclone.database.connection import SESSION
from instaclone.app.story.errors import StoryNotExistsError, StoryPermissionError, UserNotFoundError, StoryViewPermissionError

class StoryStore:
    async def get_user_from_id(self, user_id: int) -> User:
        user = await SESSION.scalar(select(User).where(User.user_id == user_id))
        if not user:
            raise UserNotFoundError()
        return user

    # @transactional
    async def add_story(
        self, 
        user: User,
        media: List["Medium"]
    ) -> Story:
        user_in_session = await SESSION.get(User, user.user_id)
        if user_in_session is None:
            user = await SESSION.merge(user)
        else:
            user = user_in_session

        story = Story(user=user, media=media, creation_date=datetime.now(timezone.utc))
        SESSION.add(story)
        await SESSION.commit()
        return story
    
    async def get_story_list(
        self,
        user: User
    ) -> Sequence["Story"]:
        query = select(Story).where(
            Story.user_id == user.user_id,
            Story.expiration_date > datetime.now(timezone.utc)
        ).order_by(Story.creation_date)

        result = await SESSION.scalars(query)
        stories = result.all()

        return stories
    
    async def get_story_by_id(
        self,
        story_id: int
    ) -> Story:
        query = select(Story).where(Story.story_id == story_id)
        story = await SESSION.scalar(query)

        if not story:
            raise StoryNotExistsError()

        return story
    
    # @transactional
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
        await SESSION.commit()
        return story

    # @transactional
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
        await SESSION.execute(delete(Medium).where(Medium.story_id == story_id))
        await SESSION.execute(delete_query)
        await SESSION.commit()
        return "SUCCESS"

    async def record_story_view(
        self,
        story_id: int,
        viewer: User
    ) -> None:
        story = await self.get_story_by_id(story_id)
        
        #if the viewer is the story owner, do nothing
        if story.user_id == viewer.user_id:
            return
        
        #check if already recorded
        query = select(StoryView).where(
            StoryView.story_id == story_id,
            StoryView.user_id == viewer.user_id
        )
        existing_view = await SESSION.scalar(query)
        
        if not existing_view:
            view = StoryView(story_id=story_id, user_id=viewer.user_id)
            SESSION.add(view)
            await SESSION.commit()
    
    # getting users who viewed story
    async def get_story_viewers(
        self,
        story_id: int,
        owner: User
    ) -> Sequence[User]:

        story = await self.get_story_by_id(story_id)
        if story.user_id != owner.user_id:
            raise StoryViewPermissionError()
        
        query = (
            select(User)
            .join(StoryView, StoryView.user_id == User.user_id)
            .where(StoryView.story_id == story_id)
            .order_by(StoryView.viewed_at.desc())
        )
        result = await SESSION.scalars(query)
        return result.all()

        