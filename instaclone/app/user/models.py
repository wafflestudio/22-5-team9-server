from typing import TYPE_CHECKING, List
from pydantic import EmailStr
from sqlalchemy import String, BigInteger, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from instaclone.database.common import Base

if TYPE_CHECKING:
    from instaclone.app.follower.models import Follower
    from instaclone.app.post.models import Post
    from instaclone.app.story.models import Story
    from instaclone.app.comment.models import Comment
    from instaclone.app.story.models import StoryView
    from instaclone.app.like.models import PostLike, StoryLike, CommentLike
    from instaclone.app.dm.models import Message

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
    gender: Mapped[str] = mapped_column(String(10), nullable=True)
    # birthday
    birthday: Mapped[Date] = mapped_column(Date, nullable=True)
    # introduce
    introduce: Mapped[str] = mapped_column(String(100), nullable=True)
    # website
    website: Mapped[str] = mapped_column(String(100), nullable=True)


    # relationships
    # 1(user) to N(others)
    follower_users: Mapped[List["Follower"]] = relationship("Follower", foreign_keys="[Follower.following_id]", back_populates="following")
    following_users: Mapped[List["Follower"]] = relationship("Follower", foreign_keys="[Follower.follower_id]", back_populates="follower")
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user", lazy="selectin")
    stories: Mapped[list["Story"]] = relationship("Story", back_populates="user", lazy="selectin")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="user")
    story_views: Mapped[list["StoryView"]] = relationship("StoryView", back_populates="user", lazy="selectin")
    post_likes: Mapped[list["PostLike"]] = relationship("PostLike", back_populates="user")
    story_likes: Mapped[list["StoryLike"]] = relationship("StoryLike", back_populates="user")
    comment_likes: Mapped[list["CommentLike"]] = relationship("CommentLike", back_populates="user")
    sent_messages: Mapped[List["Message"]] = relationship("Message", back_populates="sender", foreign_keys="[Message.sender_id]")
    received_messages: Mapped[List["Message"]] = relationship("Message", back_populates="receiver", foreign_keys="[Message.receiver_id]")

class BlockedToken(Base):
    __tablename__ = "blocked_token"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    jti: Mapped[str] = mapped_column(String(40))