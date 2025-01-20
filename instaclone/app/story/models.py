from typing import TYPE_CHECKING
from datetime import datetime, timedelta
from sqlalchemy import BigInteger, DATETIME, ForeignKey, event, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from instaclone.database.common import Base

if TYPE_CHECKING:
    from instaclone.app.user.models import User
    from instaclone.app.medium.models import Medium
    from instaclone.app.like.models import StoryLike

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
    highlights: Mapped[list["Highlight"]] = relationship(
        "Highlight", secondary="highlight_stories", back_populates="story_ids"
    )
    likes: Mapped[list["StoryLike"]] = relationship("StoryLike", back_populates="story")
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

class Highlight(Base):
    __tablename__ = "highlights"

    # highlight_id
    highlight_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    # user_id
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"))
    highlight_name: Mapped[String] = mapped_column(String(15), nullable=False)
    cover_image_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("media.image_id"))
    
    story_ids: Mapped[list[int]] = relationship("Story", secondary="highlight_stories", back_populates="highlights")
    media: Mapped["Medium"] = relationship("Medium", lazy="selectin")

class HighlightStories(Base):
    __tablename__ = "highlight_stories"

    highlight_id = mapped_column(ForeignKey("highlights.highlight_id"), primary_key=True)
    story_id = mapped_column(ForeignKey("stories.story_id"), primary_key=True)