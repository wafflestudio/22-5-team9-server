from typing import TYPE_CHECKING, Optional
from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from instaclone.database.common import Base


if TYPE_CHECKING:
    from instaclone.app.user.models import User
    from instaclone.app.post.models import Post
    from instaclone.app.like.models import CommentLike

class Comment(Base):
    __tablename__ = "comments"

    # user_id
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"))
    # post_id
    post_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("posts.post_id"))
    # comment_id
    comment_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    # parent_id
    parent_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("comments.comment_id"), nullable=True)
    # comment_text
    comment_text: Mapped[str] = mapped_column(String(200))


     # relationships
    user: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")
    replies: Mapped[list["Comment"]] = relationship("Comment", back_populates="parent", cascade="all, delete-orphan", lazy="selectin")
    parent: Mapped[Optional["Comment"]] = relationship("Comment", remote_side="Comment.comment_id", back_populates="replies")
    likes: Mapped[list["CommentLike"]] = relationship("CommentLike", back_populates="comment")