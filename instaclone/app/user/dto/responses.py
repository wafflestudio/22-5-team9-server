from typing import Self
from pydantic import BaseModel, EmailStr, HttpUrl
from sqlalchemy import Date
from datetime import date, datetime

from instaclone.app.user.models import User
from instaclone.app.post.models import Post
from instaclone.common.errors import InvalidFieldFormatError


class UserDetailResponse(BaseModel):
    user_id: int
    username: str
    full_name: str
    email: EmailStr
    phone_number: str
    creation_date: date
    profile_image: str
    gender: str
    birthday: date | None
    introduce: str | None
    website: str | None
    follwers: int
    following: int
    post_count: int
    post_ids: list[int]

    @staticmethod
    def from_user(user: User) -> "UserDetailResponse":
        if user.birthday != None and not isinstance(user.birthday, date):
            raise InvalidFieldFormatError("Expected a valid SQLAlchemy `Date` or `datetime.date` object")
        if not isinstance(user.creation_date, date):
            raise InvalidFieldFormatError("Expected a valid SQLAlchemy `Date` or `datetime.date` object")
        
        post_ids = []
        if (user.posts):
            for post in user.posts:
                post_ids.append(post.post_id)


        return UserDetailResponse(
            user_id=user.user_id,
            username=user.username,
            full_name=user.full_name,
            email=user.email,
            phone_number=user.phone_number,
            creation_date=user.creation_date,
            profile_image=user.profile_image,
            gender=user.gender,
            birthday=user.birthday,
            introduce=user.introduce,
            website=user.website,
            follwers=len(user.follower_users),
            following=len(user.following_users),
            post_count=len(user.posts),
            post_ids=post_ids
        )

class UserSigninResponse(BaseModel):
    access_token: str
    refresh_token: str