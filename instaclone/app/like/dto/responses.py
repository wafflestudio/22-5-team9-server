from pydantic import BaseModel

class LikeResponse(BaseModel):
    content_id: int
    like_type: str
    liker_ids: list[int]
