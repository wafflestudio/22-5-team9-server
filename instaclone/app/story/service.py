from typing import Annotated, Sequence, List
from fastapi import Depends, UploadFile
from uuid import uuid4
import os

from instaclone.app.story.errors import FileSizeLimitError
from instaclone.app.story.store import StoryStore
from instaclone.app.user.models import User
from instaclone.app.story.models import Story
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

    async def file_to_medium(self, file: UploadFile) -> Medium:
        """
        파일을 저장하고 medium을 생성합니다.
        """
        if len(await file.read()) > MAX_FILE_SIZE:
            raise FileSizeLimitError()
        unique_filename = f"{uuid4().hex}_{file.filename}"
        file_path = os.path.join(BASE_DIR, unique_filename)

        with open(file_path, "wb") as buffer:
            while content := await file.read(1024):
                buffer.write(content)

        medium = await self.story_store.add_medium(unique_filename, file_path)
        return medium