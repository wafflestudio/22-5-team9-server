from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column
from instaclone.database.common import Base


class Medium(Base):
    __tablename__ = "media"

    # post_id
    post_id: Mapped[int] = mapped_column(BigInteger)
    # image_id
    image_id: Mapped[int] = mapped_column(BigInteger)
    # file_name
    file_name: Mapped[str] = mapped_column(String(100))
    # url (can be modified to path)
    url: Mapped[str] = mapped_column(String(200))