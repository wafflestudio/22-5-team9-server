from typing import TYPE_CHECKING
from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from instaclone.database.common import Base


if TYPE_CHECKING:
    from instaclone.app.user.models import User
    from instaclone.app.medium.models import Medium
    from instaclone.app.comment.models import Comment

class Post(Base):
    __tablename__ = "posts"

    # user_id
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"))
    # post_id
    post_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    # location
    location: Mapped[str | None] = mapped_column(String(50), nullable=True)
    # post_text
    post_text: Mapped[str | None] = mapped_column(String(500), nullable=True)


    # relationships
    user: Mapped["User"] = relationship("User", back_populates="posts")
    # 1(story) to N(media)
    media: Mapped[list["Medium"]] = relationship("Medium", back_populates="post")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post")