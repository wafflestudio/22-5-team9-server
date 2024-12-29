from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from instaclone.database.common import Base


class Follower(Base):
    __tablename__ = "followers"

    # user_id
    user_id: Mapped[int] = mapped_column(BigInteger)
    # follower_id
    follower_id: Mapped[int] = mapped_column(BigInteger)
    # following_id
    following_id: Mapped[int] = mapped_column(BigInteger)