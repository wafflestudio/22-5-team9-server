from pydantic import BaseModel, Field
from fastapi import File, Form, UploadFile


class MediumUploadRequest(BaseModel):
    post_id: int | None = Form(None)
    story_id: int | None = Form(None)
    file: UploadFile = File(...)

    class Config:
        schema_extra = {
            "example": {
                "post_id": 1,
                "story_id": None,
                "file": "(binary image file)",
            }
        }
