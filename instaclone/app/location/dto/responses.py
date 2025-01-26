from pydantic import BaseModel

class LocationResponse(BaseModel):
    tag_id: int
    name: str
    citation: int
    