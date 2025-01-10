from pydantic import BaseModel, Field, ValidationError, root_validator
from fastapi import File, Form, UploadFile


class MediumUploadRequest(BaseModel):
    post_id: int | None = Form(None)
    story_id: int | None = Form(None)
    file: UploadFile = File(...)

    @root_validator
    def validate_medium(cls, values):
        post_id = values.get("post_id")
        story_id = values.get("story_id")

        if not post_id and not story_id:
            raise ValueError("You must provide at least one of post_id or story_id.")
        return values

    class Config:
        schema_extra = {
            "example": {
                "post_id": 1,
                "story_id": None,
                "file": "(binary image file)",
            }
        }
