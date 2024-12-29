from pydantic import EmailStr
from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from instaclone.database.common import Base


class User(Base):
    __tablename__ = "users"

    # user_id
    user_id: Mapped[int] = mapped_column(BigInteger)
    # username : nickname in insta
    username: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    # password
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    # full_name : real name
    full_name: Mapped[str] = mapped_column(String(4), nullable=False)
    # email
    email: Mapped[EmailStr] = mapped_column(String(100), unique=True, index=True)
    # phone_number : 010XXXXXXXX
    phone_number: Mapped[str] = mapped_column(String(11), unique=True)
    # creation_date : YYYY.MM.DD
    creation_date : Mapped[str] = mapped_column(String(11))