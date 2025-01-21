from typing import List, Sequence
from datetime import datetime, timezone
from sqlalchemy.sql import select, delete
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from instaclone.app.user.models import User
from instaclone.app.medium.models import Medium
from instaclone.app.story.models import Story, StoryView, Highlight, HighlightStories
from instaclone.database.connection import SESSION
from instaclone.app.story.errors import StoryNotExistsError, StoryPermissionError, UserNotFoundError, HighlightDNEError, StoryViewPermissionError, StoryInHighlightsError, HighlightNameError
from instaclone.common.errors import DebugError
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

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
        await self.clean_up(user=user, story_id=story_id)
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

        highlight_names = await SESSION.execute(
            select(Highlight.highlight_name).where(Highlight.user_id==user.user_id)
        )
        highlight_names = highlight_names.scalars().all()

        if highlight_name in highlight_names:
            raise HighlightNameError()

        highlight = Highlight(user_id=user.user_id, highlight_name=highlight_name, media=cover_image)
        try:
            SESSION.add(highlight)
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
        
        if not story:
            raise DebugError(HTTPException, "Story Invalid")

        highlight: Highlight | None = (
            await SESSION.execute(
                select(Highlight).where(Highlight.highlight_id==highlight_id).options(selectinload(Highlight.story_ids))
            )
        ).scalar_one_or_none()

        if not highlight:
            raise HighlightDNEError()
        if story.user_id != user.user_id or highlight.user_id != user.user_id:
            raise StoryPermissionError()
        
        story_ids = await SESSION.execute(
            select(HighlightStories.story_id).where(HighlightStories.highlight_id==highlight_id)
        )
        story_ids = story_ids.scalars().all()
        
        print(story_ids)
        if story_id in story_ids:
            raise StoryInHighlightsError()
        
        highlight_story: HighlightStories = HighlightStories(
            highlight_id=highlight.highlight_id, story_id=story.story_id
        )
        SESSION.add(highlight_story)

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

    async def delete_highlight(
            self,
            user: User,
            highlight_id: int
    ):
        highlight : Highlight = await self.get_highlight(highlight_id=highlight_id)
        if not highlight:
            raise HighlightDNEError()
        if highlight.user_id != user.user_id:
            raise StoryPermissionError()
        
        try:
            await SESSION.execute(
                delete(HighlightStories).where(HighlightStories.highlight_id==highlight_id)
            )
            await SESSION.execute(
                delete(Highlight).where(Highlight.highlight_id==highlight_id)
            )
            await SESSION.commit()
        except Exception as e:
            await SESSION.rollback()
            raise DebugError(HTTP_500_INTERNAL_SERVER_ERROR, "Highlight could not be deleted")
        
    async def unsave_story(
            self,
            user: User,
            highlight_id: int,
            story_id: int
    ):
        highlight: Highlight = await self.get_highlight(highlight_id=highlight_id)
        if not highlight:
            raise HighlightDNEError()
        if highlight.user_id != user.user_id:
            raise StoryPermissionError()
        story_id_results = await SESSION.execute(
            select(HighlightStories.story_id).where(HighlightStories.highlight_id==highlight.highlight_id)
        )
        story_ids = story_id_results.scalars().all()

        story: Story = await self.get_story_by_id(story_id)
        
        if story_id not in story_ids:
            raise StoryNotExistsError()

        try:
            if highlight.media in story.media and len(story_ids) > 1:
                i = 0
                while story_ids[i] == story_id:
                    i += 1
                new_cover_story: Story = await self.get_story_by_id(story_ids[i])
                highlight.media = new_cover_story.media[0]
            await SESSION.execute(
                delete(HighlightStories).where(HighlightStories.story_id==story_id, HighlightStories.highlight_id==highlight_id)
            )
            if len(story_ids) == 1:
                print("Length of stories in highlight = 1!")
                await SESSION.execute(
                    delete(Highlight).where(Highlight.highlight_id==highlight_id)
                )
            await SESSION.commit()
        except Exception as e:
            await SESSION.rollback()
            raise DebugError(HTTP_500_INTERNAL_SERVER_ERROR, "Story could not be removed from highlight")
        
    async def clean_up(self,
                        user: User,
                        story_id: int):
        highlight_ids = await SESSION.execute(
            select(HighlightStories.highlight_id).where(HighlightStories.story_id==story_id)
        )
        highlight_ids = highlight_ids.scalars().all()
        for highlight_id in highlight_ids:
            await self.unsave_story(user=user, highlight_id=highlight_id, story_id=story_id)

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
