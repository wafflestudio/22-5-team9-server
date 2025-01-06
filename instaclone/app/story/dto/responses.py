from pydantic import BaseModel
from datetime import datetime

from instaclone.app.story.models import Story

class StoryDetailResponse(BaseModel):
    story_id: int
    creation_date: datetime
    expiration_date: datetime
    user_id: int
    
    @staticmethod
    def from_story(story: Story) -> "StoryDetailResponse":
        return StoryDetailResponse(
            story_id=story.story_id,
            creation_date=story.creation_date,
            expiration_date=story.expiration_date,
            user_id=story.user_id
        )