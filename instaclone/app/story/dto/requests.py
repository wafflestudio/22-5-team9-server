from typing import List
from pydantic import BaseModel

from instaclone.app.medium.models import Medium

class StoryCreateRequest(BaseModel):
    media: List["Medium"]

class StoryEditRequest(BaseModel):
    media: List["Medium"]
