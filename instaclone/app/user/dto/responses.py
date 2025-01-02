from typing import Self
from pydantic import BaseModel, EmailStr, HttpUrl
from sqlalchemy import Date

from instaclone.app.user.models import User


class UserDetailResponse(BaseModel):
    user_id: int
    username: str
    full_name: str
    email: EmailStr
    phone_number: str
    creation_date: Date
    profile_image: str
    gender: str
    birthday: Date
    introduce: str
    website: str
    follwers: int
    following: int
    posts: int

    @staticmethod
    def from_user(user: User) -> "UserDetailResponse":
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
            posts=len(user.posts)
        )

class UserSigninResponse(BaseModel):
    access_token: str
    refresh_token: str