from datetime import datetime, timedelta
from enum import Enum
from typing import Annotated
from uuid import uuid4
from pydantic import EmailStr

from fastapi import Depends
from instaclone.app.user.errors import (
    BlockedTokenError,
    ExpiredSignatureError,
    InvalidTokenError,
    InvalidUsernameOrPasswordError,
)
from instaclone.app.auth.utils import (
    create_access_token,
    create_refresh_token
)
from instaclone.common.utils import identify_input_type
from instaclone.app.user.models import User
from instaclone.app.user.store import UserStore
import jwt

SECRET = "secret_for_jwt"


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class UserService:
    def __init__(self, user_store: Annotated[UserStore, Depends()]) -> None:
        self.user_store = user_store

    async def get_user_by_username(self, username: str) -> User | None:
        return await self.user_store.get_user_by_username(username)
    
    async def get_user_by_email(self, email: EmailStr) -> User | None:
        return await self.user_store.get_user_by_email(email)
    
    async def get_user_by_phone_number(self, phone_number: str) -> User | None:
        return await self.user_store.get_user_by_phone_number(phone_number)
    
    def validate_access_token(self, token: str) -> str:
        """
        access_token을 검증하고, username을 반환합니다.
        """
        try:
            payload = jwt.decode(
                token, SECRET, algorithms=["HS256"], options={"require": ["sub"]}
            )
            if payload["type"] != TokenType.ACCESS.value:
                raise InvalidTokenError()
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise ExpiredSignatureError()
        except jwt.InvalidTokenError:
            raise InvalidTokenError()

    async def edit_user(
        self,
        user: User,
        username : str,
        full_name: str,
        introduce: str,
        profile_image: str
    ) -> User:
        return await self.user_store.edit_user(user=user, username=username, full_name=full_name, introduce=introduce, profile_image=profile_image)
    
    async def signin(self, username: str, password: str) -> tuple[str, str]:
        username_type = identify_input_type(username)
        if username_type == "email":
            user = await self.get_user_by_email(username)
        elif username_type == "phone_number":
            user = await self.get_user_by_phone_number(username)
        elif username_type == "username":
            user = await self.get_user_by_username(username)

        if not user or user.password != password:
            raise InvalidUsernameOrPasswordError()

        access_token = create_access_token(username, expires=timedelta(minutes=10))
        refresh_token = create_refresh_token(username, expires=timedelta(hours=24))

        return access_token, refresh_token
    
    async def signup(self,
        username: str,
        password: str,
        full_name: str,
        email: EmailStr, 
        phone_number: str
    ) -> User:
        return await self.user_store.add_user(username=username, password=password, full_name=full_name, email=email, phone_number=phone_number)
