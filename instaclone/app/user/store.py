from typing import Sequence
from pydantic import EmailStr
from sqlalchemy.sql import select
from sqlalchemy.orm import joinedload

from instaclone.app.user.models import User
from instaclone.database.annotation import transactional
from instaclone.database.connection import SESSION


class UserStore:
    async def get_user_by_username(self, username: str) -> User | None:
        return await SESSION.scalar(select(User).where(User.username == username))
    
    async def get_user_by_email(self, email: EmailStr) -> User | None:
        return await SESSION.scalar(select(User).where(User.email == email))
    
    async def get_user_by_phone_number(self, phone_number: str) -> User | None:
        return await SESSION.scalar(select(User).where(User.phone_number == phone_number))
    
    @transactional
    async def edit_user(
        self, 
        user: User,
        username : str,
        full_name: str,
        introduce: str,
        profile_image: str
    ) -> User:
        user.username = username
        user.full_name = full_name
        user.introduce = introduce
        user.profile_image = profile_image
        SESSION.add(user)
        return user