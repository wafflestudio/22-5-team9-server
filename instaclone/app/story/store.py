from typing import List, Sequence
from datetime import datetime, timezone
from sqlalchemy.sql import select, delete
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from instaclone.app.user.models import User
from instaclone.app.medium.models import Medium
from instaclone.app.story.models import Story, Highlight, HighlightStories
from instaclone.database.annotation import transactional
from instaclone.database.connection import SESSION
from instaclone.app.story.errors import StoryNotExistsError, StoryPermissionError, UserNotFoundError, HighlightDNEError
from instaclone.common.errors import DebugError

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
    
    async def create_highlight(
            self,
            user: User,
            highlight_name: str,
            cover_image: Medium
    ) -> Highlight:
        user_in_session = await SESSION.get(User, user.user_id)
        if user_in_session is None:
            user = await SESSION.merge(user)
        else:
            user = user_in_session

        highlight = Highlight(user_id=user.user_id, highlight_name=highlight_name, media=cover_image)
        SESSION.add(highlight)
        try:
            await SESSION.commit()
        except HTTPException as e:
            await SESSION.rollback()
            raise DebugError(e.status_code, e.detail)
        return highlight
    
    async def add_story_highlight(
            self,
            user: User,
            story_id: int,
            highlight_id: int
    ) -> Highlight:
        story : Story = await self.get_story_by_id(story_id)

        highlight: Highlight | None = (
            await SESSION.execute(
                select(Highlight).where(Highlight.highlight_id==highlight_id).options(selectinload(Highlight.story_ids))
            )
        ).scalar_one_or_none()

        if not highlight:
            raise HighlightDNEError()
        if story.user_id != user.user_id or highlight.user_id != user.user_id:
            raise PermissionError()
        
        highlight_story: HighlightStories = HighlightStories(
            highlight_id=highlight.highlight_id, story_id=story.story_id
        )
        SESSION.add(highlight_story)

        if not story:
            raise DebugError(HTTPException, "Story Invalid")

        try:
            await SESSION.commit()
            await SESSION.refresh(highlight)
        except HTTPException as e:
            await SESSION.rollback()
            raise DebugError(e.status_code, e.detail)
        return highlight
    
    async def get_highlight_list(self, user_id: int) -> Sequence["Highlight"]:
        query = select(Highlight).where(Highlight.user_id == user_id)

        result = await SESSION.scalars(query)
        highlights = result.all()

        return highlights
    
    async def get_highlight(self, highlight_id):
        query = select(Highlight).where(Highlight.highlight_id == highlight_id)
        highlight = await SESSION.scalar(query)

        if not highlight:
            raise HighlightDNEError()

        return highlight

    async def edit_highlight():
        pass

    async def delete_highlight():
        pass