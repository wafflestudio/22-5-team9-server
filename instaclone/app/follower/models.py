from typing import TYPE_CHECKING
from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from instaclone.database.common import Base

if TYPE_CHECKING:
    from instaclone.app.user.models import User

class Follower(Base):
    __tablename__ = "followers"

    follower_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"), primary_key=True)
    following_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"), primary_key=True)

    # "follower" -> the User who follows
    follower: Mapped["User"] = relationship("User", foreign_keys=[follower_id], back_populates="following_users")
    # "following" -> the User being followed
    following: Mapped["User"] = relationship("User", foreign_keys=[following_id], back_populates="follower_users")