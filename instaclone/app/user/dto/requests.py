from pydantic import BaseModel

class UserSigninRequest(BaseModel):
    username: str
    password: str