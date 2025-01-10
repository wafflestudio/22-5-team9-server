from typing import TYPE_CHECKING, Optional
from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from instaclone.database.common import Base

if TYPE_CHECKING:
    from instaclone.app.post.models import Post
    from instaclone.app.story.models import Story
    
class Medium(Base):
    __tablename__ = "media"

    # post_id
    post_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("posts.post_id", ondelete='CASCADE'), nullable=True)
    # story_id
    story_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("stories.story_id", ondelete='CASCADE'), nullable=True)
    # image_id
    image_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    # file_name
    file_name: Mapped[str] = mapped_column(String(100))
    # url (can be modified to path)
    url: Mapped[str] = mapped_column(String(200))
    # # file_type (image, video, gif, ...)
    # file_type: Mapped[str] = mapped_column(String(20), nullable=False)



    # relationships
    post: Mapped[Optional["Post"]] = relationship("Post", back_populates="media")
    story: Mapped[Optional["Story"]] = relationship("Story", back_populates="media")
