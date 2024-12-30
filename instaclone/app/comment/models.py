from sqlalchemy import BigInteger, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from instaclone.database.common import Base


class Comment(Base):
    __tablename__ = "comments"

    # user_id
    user_id: Mapped[int] = mapped_column(BigInteger)
    # post_id
    post_id: Mapped[int] = mapped_column(BigInteger)
    # comment_id
    comment_id: Mapped[int] = mapped_column(BigInteger)
    # parent_id
    parent_id: Mapped[int] = mapped_column(BigInteger)
    # comment_text
    comment_text: Mapped[str] = mapped_column(String(200))