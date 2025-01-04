from typing import Sequence
from datetime import datetime
from pydantic import EmailStr
from sqlalchemy.sql import select
from sqlalchemy.orm import joinedload

from instaclone.app.user.models import User
from instaclone.database.annotation import transactional
from instaclone.database.connection import SESSION
from instaclone.app.user.errors import UsernameAlreadyExistsError, EmailAlreadyExistsError, PhoneNumberAlreadyExistsError


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
        username : str | None,
        full_name: str | None,
        introduce: str | None,
        profile_image: str | None
    ) -> User:
        user_in_session = await SESSION.get(User, user.user_id)  # Load the user from the current session
        if user_in_session is None:
            # If the user is not in the session, merge it into the current session
            user = await SESSION.merge(user)

        if username:
            user.username = username
        if full_name:
            user.full_name = full_name
        if introduce:
            user.introduce = introduce
        if profile_image:
            user.profile_image = profile_image

        await SESSION.flush()
        return user
    
    @transactional
    async def add_user(
        self,
        username: str,
        password: str,
        full_name: str,
        email: EmailStr,
        phone_number: str
    ) -> User:
        if await self.get_user_by_username(username):
            raise UsernameAlreadyExistsError()
        if await self.get_user_by_email(email):
            raise EmailAlreadyExistsError()
        if await self.get_user_by_phone_number(phone_number):
            raise PhoneNumberAlreadyExistsError()
        user = User(username=username, password=password, full_name=full_name, email=email, phone_number=phone_number, creation_date=datetime.today().date(), profile_image="test_image", gender="test", birthday=datetime.today().date(), introduce="test", website="test")
        SESSION.add(user)
        return user
