from sqlalchemy import BigInteger, Integer, DATETIME
from sqlalchemy.orm import Mapped, mapped_column
from instaclone.database.common import Base


class Story(Base):
    __tablename__ = "stories"

    # user_id
    user_id: Mapped[int] = mapped_column(BigInteger)
    # story_id
    story_id: Mapped[int] = mapped_column(BigInteger)
    # expiration_date : YYYY-MM-DD HH:MM:SS
    expiration_date: Mapped[DATETIME] = mapped_column(DATETIME)

