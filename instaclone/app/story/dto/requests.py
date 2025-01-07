from typing import List
from pydantic import BaseModel
from fastapi import UploadFile

class StoryCreateRequest(BaseModel):
    media: List[UploadFile]

class StoryEditRequest(BaseModel):
    media: List[UploadFile]
