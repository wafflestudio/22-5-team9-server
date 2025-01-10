from pydantic import BaseModel, HttpUrl


class MediumResponse(BaseModel):
    image_id: int
    post_id: int | None
    #story_id: int | None
    file_name: str
    url: str
