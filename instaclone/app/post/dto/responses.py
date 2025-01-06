from datetime import datetime
from pydantic import BaseModel

class PostDetailResponse(BaseModel):
    post_id: int
    user_id: int
    location: str | None
    post_text: str | None
    creation_date: datetime
