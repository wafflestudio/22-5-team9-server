from pydantic import BaseModel
from typing import Optional

class LocationRequest(BaseModel):
    tag_id: Optional[int] = 1
    expiration_delta: Optional[int] = 1
    expiration_unit: Optional[str] = "hours"