from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlalchemy import BigInteger, ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from instaclone.database.common import Base

if TYPE_CHECKING:
    from instaclone.app.post.models import Post
    from instaclone.app.story.models import Story
    from instaclone.app.comment.models import Comment
    from instaclone.app.user.models import User

class PostLike(Base):
    __tablename__ = "post_likes"

    like_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"))
    content_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("posts.post_id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="post_likes")
    post: Mapped["Post"] = relationship("Post", back_populates="likes", passive_deletes=True)

class StoryLike(Base):
    __tablename__ = "story_likes"

    like_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"))
    content_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("stories.story_id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="story_likes")
    story: Mapped["Story"] = relationship("Story", back_populates="likes", passive_deletes=True)

class CommentLike(Base):
    __tablename__ = "comment_likes"

    like_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"))
    content_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("comments.comment_id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="comment_likes")
    comment: Mapped["Comment"] = relationship("Comment", back_populates="likes", passive_deletes=True)
