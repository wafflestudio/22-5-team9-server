from typing import TYPE_CHECKING, List
from pydantic import EmailStr
from enum import Enum
from sqlalchemy import String, BigInteger, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from instaclone.database.common import Base

if TYPE_CHECKING:
    #from instaclone.app.follower.models import Follower
    from instaclone.app.post.models import Post
    from instaclone.app.story.models import Story
    from instaclone.app.comment.models import Comment

# class Gender(str, Enum):
#     male = "M"
#     female = "F"
#     none = "N"

class Follower(Base):
    __tablename__ = "followers"

    follower_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.user_id"), primary_key=True
    )
    following_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.user_id"), primary_key=True
    )

    # "follower" -> the User who follows
    follower: Mapped["User"] = relationship(
        "User",
        foreign_keys=[follower_id],
        back_populates="following_users",
    )
    # "following" -> the User being followed
    following: Mapped["User"] = relationship(
        "User",
        foreign_keys=[following_id],
        back_populates="follower_users",
    )


class User(Base):
    __tablename__ = "users"

    # user_id
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    # username : nickname in insta
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    # password
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    # full_name : real name
    full_name: Mapped[str] = mapped_column(String(30), nullable=False)
    # email
    email: Mapped[EmailStr] = mapped_column(String(100), unique=True)
    # phone_number : 010XXXXXXXX
    phone_number: Mapped[str] = mapped_column(String(11), unique=True)
    # creation_date : YYYY-MM-DD
    creation_date: Mapped[Date] = mapped_column(Date)
    # profile_image : file path string
    profile_image: Mapped[str] = mapped_column(String(100))

    # gender
    # gender : Mapped[Enum] = mapped_column(Gender)
    gender: Mapped[str] = mapped_column(String(10))
    # birthday
    birthday: Mapped[Date] = mapped_column(Date)
    # introduce
    introduce: Mapped[str] = mapped_column(String(100))
    # website
    website: Mapped[str] = mapped_column(String(100))


    # relationships
    # 1(user) to N(others)
    follower_users: Mapped[List["Follower"]] = relationship(
        "Follower",
        foreign_keys="[Follower.following_id]",  # string-based to avoid import issues
        back_populates="following",
        lazy="selectin"
    )
    following_users: Mapped[List["Follower"]] = relationship(
        "Follower",
        foreign_keys="[Follower.follower_id]",
        back_populates="follower",
        lazy="selectin"
    )
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user", lazy="selectin")
    #stories: Mapped[list["Story"]] = relationship("Story", back_populates="user")
    #comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="user")
