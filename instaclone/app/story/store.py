from typing import List, Sequence
from datetime import datetime, timezone
from sqlalchemy.sql import select, delete
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from instaclone.app.user.models import User
from instaclone.app.medium.models import Medium
from instaclone.app.story.models import Story, StoryView, Highlight, HighlightStories, HighlightSubusers
from instaclone.database.connection import SESSION
from instaclone.app.story.errors import StoryNotExistsError, StoryPermissionError, UserNotFoundError, HighlightDNEError, StoryViewPermissionError, StoryInHighlightsError, HighlightNameError, HighlightPermissionError, UserAddedError, CannotRemoveError, CannotChangeAdminError, CannotChangeHighlightNameError, StoryPermissionAccessError
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
        
        highlight_users = await SESSION.execute(
            select(HighlightSubusers.user_id).where(HighlightSubusers.highlight_id==highlight.highlight_id)
        )
        highlight_users = highlight_users.scalars().all()

        if user.user_id not in highlight_users:
            raise HighlightPermissionError()

        if story.user_id != user.user_id:
            raise StoryPermissionAccessError()
        
        story_ids = await SESSION.execute(
            select(HighlightStories.story_id).where(HighlightStories.highlight_id==highlight_id)
        )
        story_ids = story_ids.scalars().all()
        
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
    
    async def add_init_user_highlight(
            self,
            user: User,
            highlight: Highlight
    ):
        highlight_user = HighlightSubusers(highlight_id=highlight.highlight_id, user_id=user.user_id)

        try:
            SESSION.add(highlight_user)
            await SESSION.commit()
            await SESSION.refresh(highlight)
        except HTTPException as e:
            await SESSION.rollback()
            raise DebugError(e.status_code, e.detail)
        
        return highlight
    
    async def add_user_highlight(
            self,
            user: User,
            user_id: int,
            highlight_id: int
    ) -> Highlight:
        highlight: Highlight = await self.get_highlight(highlight_id)

        if highlight.user_id != user.user_id:
            raise HighlightPermissionError()
        
        highlight_users = await SESSION.scalars(select(HighlightSubusers.user_id).where(HighlightSubusers.highlight_id==highlight_id))
        highlight_users = highlight_users.all()

        # if user.user_id not in highlight_users:
        #     raise HighlightPermissionError()      # Give permission to add users to non-admin

        if user_id in highlight_users:
            raise UserAddedError()
        
        highlight_user = HighlightSubusers(highlight_id=highlight_id, user_id=user_id)

        try:
            SESSION.add(highlight_user)
            await SESSION.commit()
            await SESSION.refresh(highlight)
        except HTTPException as e:
            await SESSION.rollback()
            raise DebugError(e.status_code, e.detail)
        
        return highlight

    
    async def get_highlight_list(self, user_id: int) -> list["Highlight"]:
        highlight_id_results = await SESSION.execute(
            select(HighlightSubusers.highlight_id).where(HighlightSubusers.user_id==user_id)
        )
        highlight_ids = highlight_id_results.scalars().all()

        highlights = []

        for highlight_id in highlight_ids:
            highlights.append(await self.get_highlight(highlight_id=highlight_id))

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
            raise HighlightPermissionError()
        
        try:
            await SESSION.execute(
                delete(HighlightStories).where(HighlightStories.highlight_id==highlight_id)
            )
            await SESSION.execute(
                delete(HighlightSubusers).where(HighlightSubusers.highlight_id==highlight_id)
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
        # Check Highlight exists
        highlight: Highlight = await self.get_highlight(highlight_id=highlight_id)
        if not highlight:
            raise HighlightDNEError()
        
        # Check story in highlights
        story_id_results = await SESSION.execute(
            select(HighlightStories.story_id).where(HighlightStories.highlight_id==highlight.highlight_id)
        )
        story_ids = story_id_results.scalars().all()

        if story_id not in story_ids:
            raise StoryNotExistsError()
        
        # Check permission
        story: Story = await self.get_story_by_id(story_id)
        
        if story.user_id != user.user_id:
            print(story.user_id)
            print(user.user_id)
            raise StoryPermissionAccessError()
        
        # Try delete
        try:
            # Deletion handling for cover image
            if highlight.media in story.media and len(story_ids) > 1:
                i = 0
                while story_ids[i] == story_id:
                    i += 1
                new_cover_story: Story = await self.get_story_by_id(story_ids[i])
                highlight.media = new_cover_story.media[0]
            await SESSION.execute(
                delete(HighlightStories).where(HighlightStories.story_id==story_id, HighlightStories.highlight_id==highlight_id)
            )
            # Delete highlight if there are no stories
            if len(story_ids) == 1:
                # Remove all users from highlight before delete
                await self.remove_all_highlight_users(highlight=highlight)
                await SESSION.execute(
                    delete(Highlight).where(Highlight.highlight_id==highlight_id)
                )
            await SESSION.commit()
        except Exception as e:
            await SESSION.rollback()
            raise DebugError(HTTP_500_INTERNAL_SERVER_ERROR, "Story could not be removed from highlight")
    
    async def remove_all_highlight_users(
            self,
            highlight: Highlight
    ):
        try:
            await SESSION.execute(
                delete(HighlightSubusers).where(HighlightSubusers.highlight_id==highlight.highlight_id)
            )
            await SESSION.commit()
        except HTTPException as e:
            await SESSION.rollback()
            raise DebugError(e.status_code, e.detail)
        
    async def remove_highlight_user(
            self,
            user: User,
            highlight_id: int,
            user_id: int
    ):
        highlight : Highlight = await self.get_highlight(highlight_id=highlight_id)

        subuser_results = await SESSION.execute(
            select(HighlightSubusers.user_id).where(HighlightSubusers.highlight_id==highlight_id)
        )

        subusers = subuser_results.scalars().all()

        if highlight.user_id != user.user_id and user.user_id != user_id:
            raise CannotRemoveError("Removing others is only permitted for admin")
        
        if user_id not in subusers:
            raise CannotRemoveError("User not added to highlight")
        
        if user_id == highlight.user_id:
            raise CannotRemoveError("Cannot remove admin from highlight.")
        
        stories = await SESSION.execute(
            select(HighlightStories.story_id)
            .join(Story, Story.story_id==HighlightStories.story_id)
            .join(HighlightSubusers, HighlightStories.highlight_id==HighlightSubusers.highlight_id)
            .where(
                   HighlightStories.highlight_id==highlight_id,
                   HighlightSubusers.user_id==user_id,
                   HighlightSubusers.user_id==Story.user_id,
                   Story.user_id==user_id)
        )
        stories = stories.scalars().all()

        print(stories)

        try:
            for story in stories:
                if user.user_id != user_id:
                    tmp_user : User = await self.get_user_from_id(user_id)
                    print(tmp_user.user_id)
                await self.unsave_story(user=tmp_user, highlight_id=highlight_id, story_id=story)
            
            await SESSION.execute(
                delete(HighlightSubusers).where(HighlightSubusers.user_id==user_id)
            )
            await SESSION.commit()
            await SESSION.refresh(highlight)
        except HTTPException as e:
            raise DebugError(e.status_code, e.detail)
        
    async def change_highlight_admin(
            self,
            user: User,
            highlight_id: int,
            user_id: int
    ):
        highlight : Highlight = await self.get_highlight(highlight_id=highlight_id)

        if user.user_id != highlight.user_id:
            raise CannotChangeAdminError("requires admin permissions")
        
        if user.user_id == user_id:
            raise CannotChangeAdminError("user already admin")
        
        users = await SESSION.execute(
            select(HighlightSubusers.user_id).where(HighlightSubusers.highlight_id==highlight_id)
        )

        users = users.scalars().all()

        if user_id not in users:
            raise CannotChangeAdminError("add user to highlight first")
        
        try:
            highlight.user_id = user_id
            await SESSION.commit()
            await SESSION.refresh(highlight)
        except HTTPException as e:
            raise DebugError(e.status_code, e.detail)
        
        return highlight
    
    async def change_highlight_name(
            self,
            user: User,
            highlight_id: int,
            highlight_name: str
    ):
        highlight : Highlight = await self.get_highlight(highlight_id=highlight_id)

        if user.user_id != highlight.user_id:
            raise CannotChangeHighlightNameError("requires admin permissions")
        
        user_ids = await SESSION.execute(
            select(HighlightSubusers.user_id).where(HighlightSubusers.highlight_id==highlight_id)
        )
        user_ids = user_ids.scalars().all()
        
        highlight_names = await SESSION.execute(
            select(Highlight.highlight_name).where(Highlight.user_id.in_(user_ids))
        )
        highlight_names = highlight_names.scalars().all()

        if highlight_name in highlight_names:
            raise HighlightNameError()
        
        try:
            highlight.highlight_name = highlight_name
            await SESSION.commit()
            await SESSION.refresh(highlight)
        except HTTPException as e:
            raise DebugError(e.status_code, e.detail)
        
        return highlight

        
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
