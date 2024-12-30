from pydantic import EmailStr
from enum import Enum
from sqlalchemy import String, BigInteger, Date
from sqlalchemy.orm import Mapped, mapped_column
from instaclone.database.common import Base

# class Gender(str, Enum):
#     male = "M"
#     female = "F"
#     none = "N"

class User(Base):
    __tablename__ = "users"

    # user_id
    user_id: Mapped[int] = mapped_column(BigInteger)
    # username : nickname in insta
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    # password
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    # full_name : real name
    full_name: Mapped[str] = mapped_column(String(4), nullable=False)
    # email
    email: Mapped[EmailStr] = mapped_column(String(100), unique=True)
    # phone_number : 010XXXXXXXX
    phone_number: Mapped[str] = mapped_column(String(11), unique=True)
    # creation_date : YYYY-MM-DD
    creation_date: Mapped[Date] = mapped_column(Date)

    # # gender
    # # gender : Mapped[Enum] = mapped_column(Gender)
    # gender: Mapped[str] = mapped_column(String(10))
    # # birthday
    # birthday: Mapped[Date] = mapped_column(Date)
    # # profile_image : file path string
    # profile_image: Mapped[str] = mapped_column(String(100))
    # # introduce
    # introduce: Mapped[str] = mapped_column(String(100))
    # # website
    # website: Mapped[str] = mapped_column(String(100))
