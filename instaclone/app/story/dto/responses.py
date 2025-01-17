from __future__ import annotations
from typing import List, Sequence
from pydantic import BaseModel
from datetime import datetime

from instaclone.app.story.models import Story, Highlight, HighlightStories
from instaclone.app.medium.models import Medium
from instaclone.database.connection import SESSION
from sqlalchemy.future import select

class StoryDetailResponse(BaseModel):
    story_id: int
    creation_date: datetime
    expiration_date: datetime
    user_id: int
    file_url: List[str]
    
    @staticmethod
    def from_story(story: Story) -> "StoryDetailResponse":
        file_urls = [m.url for m in story.media]
        return StoryDetailResponse(
            story_id=story.story_id,
            creation_date=story.creation_date,
            expiration_date=story.expiration_date,
            user_id=story.user_id,
            file_url=file_urls
        )
    
class HighlightDetailResponse(BaseModel):
    highlight_id: int
    highlight_name: str
    cover_image: str
    story_ids: Sequence[int]

    @staticmethod
    async def from_highlight(highlight: Highlight):
        # Try accessing stories safely
        story_id_results = await SESSION.execute(
            select(HighlightStories.story_id).where(HighlightStories.highlight_id==highlight.highlight_id)
        )
        story_ids = story_id_results.scalars().all()

        return HighlightDetailResponse(
            highlight_id=highlight.highlight_id,
            highlight_name=str(highlight.highlight_name),
            cover_image=highlight.media.url,
            story_ids=story_ids
        )
    
    class Config:
        orm_mode = True

StoryDetailResponse.model_rebuild()
HighlightDetailResponse.model_rebuild()