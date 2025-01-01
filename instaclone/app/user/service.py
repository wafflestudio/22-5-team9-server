from typing import Annotated
from datetime import timedelta
from fastapi import Depends

from instaclone.app.user.store import UserStore
from instaclone.app.auth.utils import (
    create_access_token,
    create_refresh_token
)
from instaclone.app.common.utils import identify_input_type
from instaclone.app.common.errors import (
    InvalidCredentialsError
)

class UserService:
    def __init__(self, user_store: Annotated[UserStore, Depends()]):
        self.user_store = user_store

    async def signin(self, username: str, password: str) -> tuple[str, str]:
        username_type = identify_input_type(username)
        if username_type == "email":
            user = await self.user_store.get_user_by_email(username)
        elif username_type == "phone_number":
            user = await self.user_store.get_user_by_phone_number(username)
        elif username_type == "username":
            user = await self.user_store.get_user_by_username(username)

        if not user or user.password != password:
            raise InvalidCredentialsError()

        access_token = create_access_token(username, expires=timedelta(minutes=10))
        refresh_token = create_refresh_token(username, expires=timedelta(hours=24))

        return access_token, refresh_token