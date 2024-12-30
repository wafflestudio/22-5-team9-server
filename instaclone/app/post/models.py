from sqlalchemy import BigInteger, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from instaclone.database.common import Base


class Post(Base):
    __tablename__ = "posts"

    # user_id
    user_id: Mapped[int] = mapped_column(BigInteger)
    # post_id
    post_id: Mapped[int] = mapped_column(BigInteger)
    # location
    location: Mapped[str] = mapped_column(String(50))
    # post_text
    post_text: Mapped[str] = mapped_column(String(500))