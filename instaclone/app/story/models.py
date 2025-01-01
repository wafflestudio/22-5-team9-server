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
    media: Mapped[list["Medium"]] = relationship("Medium", back_populates="story")
    
    
    @staticmethod
    def calculate_expiration_date(creation_date: datetime) -> datetime:
        return creation_date + timedelta(hours=24)
    
@event.listens_for(Story, "before_insert")
def set_expiration_date(_, __, target: Story):
    if target.expiration_date is None:
        target.expiration_date = target.calculate_expiration_date(target.creation_date)
