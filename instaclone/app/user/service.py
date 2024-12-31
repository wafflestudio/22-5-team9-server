from datetime import datetime, timedelta
from enum import Enum
from typing import Annotated
from uuid import uuid4

from fastapi import Depends
from instaclone.app.user.errors import (
    BlockedTokenError,
    ExpiredSignatureError,
    InvalidTokenError,
    InvalidUsernameOrPasswordError,
)
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
    
    def validate_access_token(self, token: str) -> str:
        """
        access_token을 검증하고, username을 반환합니다.
        """
        try:
            payload = jwt.decode(
                token, SECRET, algorithms=["HS256"], options={"require": ["sub"]}
            )
            if payload["typ"] != TokenType.ACCESS.value:
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