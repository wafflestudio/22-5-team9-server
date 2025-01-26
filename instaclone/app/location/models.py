from instaclone.database.common import Base
from instaclone.app.user.models import User
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

class LocationTag(Base):
    __tablename__ = "location_tags"

    location_id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    citation_count: Mapped[int] = mapped_column(Integer, server_default="0", nullable=False)

    users: Mapped[list["User"]] = relationship("User", back_populates="current_location")