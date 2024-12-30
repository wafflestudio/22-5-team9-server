from typing import TYPE_CHECKING
from sqlalchemy import BigInteger, DATETIME, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from instaclone.database.common import Base

if TYPE_CHECKING:
    from instaclone.app.user.models import User
    from instaclone.app.medium.models import Medium

class Story(Base):
    __tablename__ = "stories"

    # user_id
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"))
    # story_id
    story_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    # expiration_date : YYYY-MM-DD HH:MM:SS
    expiration_date: Mapped[DATETIME] = mapped_column(DATETIME)


    # relationships
    user: Mapped["User"] = relationship("User", back_populates="stories")
    # 1(story) to N(media)
    media: Mapped[list["Medium"]] = relationship("Medium", back_populates="story")
    