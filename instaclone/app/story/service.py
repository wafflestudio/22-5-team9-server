from typing import Annotated, Sequence, List
from fastapi import Depends, UploadFile, File
from uuid import uuid4
import os

from instaclone.app.story.errors import FileSizeLimitError
from instaclone.app.story.store import StoryStore
from instaclone.app.user.models import User
from instaclone.app.story.models import Story, Highlight
from instaclone.app.medium.models import Medium

MAX_FILE_SIZE = 10 * 1024 * 1024
BASE_DIR = "story_uploads"
os.makedirs(BASE_DIR, exist_ok=True)

class StoryService:
    def __init__(self, story_store: Annotated[StoryStore, Depends()]):
        self.story_store = story_store

    async def create_story(self, user: User, media: List["Medium"]) -> Story:
        story = await self.story_store.add_story(user, media)
        return story
    
    async def get_story(self, story_id: int) -> Story:
        story = await self.story_store.get_story_by_id(story_id)
        return story
    
    async def get_story_list(self, user_id: int) -> Sequence["Story"]:
        user = await self.story_store.get_user_from_id(user_id)
        story_list = await self.story_store.get_story_list(user)
        return story_list
    
    async def edit_story(self, user: User, story_id: int, media: List["Medium"]) -> Story:
        edited_story = await self.story_store.edit_story(user, media, story_id)
        return edited_story
    
    async def delete_story(self, user: User, story_id: int):
        await self.story_store.delete_story(user, story_id)

    async def create_highlight(self, user: User,  highlight_name: str, highlight_cover: Medium) -> Highlight:
        highlight = await self.story_store.create_highlight(user=user, highlight_name=highlight_name, cover_image=highlight_cover)
        return highlight
    
    async def add_story_highlight(self, user: User, story_id: int, highlight_id: int) -> Highlight:
        updated_highlight: Highlight = await self.story_store.add_story_highlight(user=user, story_id=story_id, highlight_id=highlight_id)
        return updated_highlight
    
    async def get_highlight(self, highlight_id) -> Highlight:
        return await self.story_store.get_highlight(highlight_id=highlight_id)

    async def get_highlight_list(self, user_id: int) -> Sequence["Highlight"]:
        return await self.story_store.get_highlight_list(user_id=user_id)
    
    async def edit_highlight():
        pass

    async def delete_highlight(
            self,
            user: User,
            highlight_id: int
    ):
        await self.story_store.delete_highlight(user=user, highlight_id=highlight_id)

    async def unsave_story(
            self,
            user: User,
            highlight_id: int,
            story_id: int
    ):
        await self.story_store.unsave_story(user=user, highlight_id=highlight_id, story_id=story_id)