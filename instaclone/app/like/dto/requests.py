from pydantic import BaseModel

class LikeRequest(BaseModel):
    content_id: int
