from pydantic import EmailStr
from sqlalchemy.sql import select

from instaclone.app.user.models import User
from instaclone.database.annotation import transactional
from instaclone.database.connection import SESSION

class UserStore:
    async def get_user_by_username(self, username: str) -> User:
        return await SESSION.scalar(select(User).where(User.username == username))
    
    async def get_user_by_email(self, email: EmailStr) -> User:
        return await SESSION.scalar(select(User).where(User.email == email))
    
    async def get_user_by_phone_number(self, phone_number: str) -> User:
        return await SESSION.scalar(select(User).where(User.phone_number == phone_number))


