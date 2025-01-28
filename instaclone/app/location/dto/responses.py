from pydantic import BaseModel
from typing import Optional

class LocationResponse(BaseModel):
    tag_id: int
    name: str
    citation: int
    owner: Optional[int]
    