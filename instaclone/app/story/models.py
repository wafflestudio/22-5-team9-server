from typing import TYPE_CHECKING
from datetime import datetime, timedelta
from sqlalchemy import BigInteger, DATETIME, ForeignKey, event
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
    # creation_date : YYYY-MM-DD
    creation_date: Mapped[datetime] = mapped_column(DATETIME, default=datetime.utcnow)
    # expiration_date
    expiration_date: Mapped[datetime] = mapped_column(DATETIME, nullable=False)


    # relationships
    user: Mapped["User"] = relationship("User", back_populates="stories")
    # 1(story) to N(media)
    media: Mapped[list["Medium"]] = relationship("Medium", back_populates="story", lazy="selectin")
    
    views: Mapped[list["StoryView"]] = relationship("StoryView", back_populates="story",lazy="selectin")
    
    @staticmethod
    def calculate_expiration_date(creation_date: datetime) -> datetime:
        return creation_date + timedelta(hours=24)
    
class StoryView(Base):
    __tablename__ = "story_views"

    story_view_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    story_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("stories.story_id"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.user_id"), nullable=False
    )
    viewed_at: Mapped[datetime] = mapped_column(
        DATETIME, default=datetime.utcnow, nullable=False
    )

    story: Mapped["Story"] = relationship("Story", back_populates="views", lazy="selectin")
    user: Mapped["User"] = relationship("User", back_populates="story_views", lazy="selectin")

    #views: Mapped[list["StoryView"]] = relationship("StoryView", back_populates="story", lazy="selectin")
    
@event.listens_for(Story, "before_insert")
def set_expiration_date(_, __, target: Story):
    if target.expiration_date is None:
        target.expiration_date = target.calculate_expiration_date(target.creation_date)
