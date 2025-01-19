from typing import TYPE_CHECKING
from datetime import datetime, timezone
from sqlalchemy import BigInteger, DateTime, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from instaclone.database.common import Base

if TYPE_CHECKING:
    from instaclone.app.user.models import User

class Message(Base):
    __tablename__ = "messages"

    message_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    sender_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"), nullable=False)
    receiver_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"), nullable=False)
    text: Mapped[str] = mapped_column(String(200), nullable=False)
    creation_date: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now(timezone.utc))

    #relationships
    sender: Mapped["User"] = relationship("User", back_populates="sent_messages", foreign_keys=[sender_id])
    receiver: Mapped["User"] = relationship("User", back_populates="received_messages", foreign_keys=[receiver_id])
