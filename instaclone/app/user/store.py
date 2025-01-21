from typing import Sequence
from datetime import datetime, date
from pydantic import EmailStr
from sqlalchemy.sql import select
from sqlalchemy.orm import joinedload, selectinload

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
    
    async def edit_user(
        self, 
        user: User,
        username : str | None,
        full_name: str | None,
        introduce: str | None,
        profile_image: str | None,
        website: str | None,
        gender: str | None
    ) -> User:
        user_in_session = await SESSION.get(User, user.user_id)  # Load the user from the current session
        if user_in_session is None:
            # If the user is not in the session, merge it into the current session
            user = await SESSION.merge(user)
        else:
            user = user_in_session

        if username:
            user.username = username
        if full_name:
            user.full_name = full_name
        if introduce:
            user.introduce = introduce
        if profile_image:
            user.profile_image = profile_image
        if website:
            user.website = website
        if gender:
            user.gender = gender

        await SESSION.commit()
        return user
    
    async def add_user(
        self,
        username: str,
        password: str,
        full_name: str,
        email: EmailStr,
        phone_number: str,
        gender: str | None = None,
        birthday: date | None = None,
        profile_image: str | None = None,
        introduce: str | None = None,
        website: str | None = None
    ) -> User:
        image_path = profile_image
        if await self.get_user_by_username(username):
            raise UsernameAlreadyExistsError()
        if await self.get_user_by_email(email):
            raise EmailAlreadyExistsError()
        if await self.get_user_by_phone_number(phone_number):
            raise PhoneNumberAlreadyExistsError()
        
        if image_path is None:
            image_path = "media_uploads/default.jpg"

        user = User(username=username, password=password, full_name=full_name, email=email, phone_number=phone_number, creation_date=datetime.today().date(), profile_image=image_path, gender=gender, birthday=birthday, introduce=introduce, website=website)
        SESSION.add(user)
        await SESSION.commit()
        return user
    
    async def search_users(self, query: str) -> list[User]:
        stmt = (
            select(User)
            .where(User.username.like(f"{query}%"))
            .order_by(User.username.asc())
            #.limit(50)  
        )
        result = await SESSION.scalars(stmt)
        return result.all()
