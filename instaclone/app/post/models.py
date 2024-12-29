from sqlalchemy import BigInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column
from instaclone.database.common import Base


class Post(Base):
    __tablename__ = "posts"

    # user_id
    user_id: Mapped[int] = mapped_column(BigInteger)
    # story_id
    story_id: Mapped[int] = mapped_column(BigInteger)
    # expiration_date
    expiration_date: Mapped[int] = mapped_column(Integer)