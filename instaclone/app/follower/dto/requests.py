from pydantic import BaseModel

class FollowRequest(BaseModel):
    follow_id: int