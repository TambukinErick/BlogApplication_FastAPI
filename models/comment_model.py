import enum
import datetime
from typing import Optional, List, Literal, get_args
from sqlalchemy import ForeignKey, String, DateTime, Enum
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from ..database import Base

class CommentModel(Base):
    __tablename__ = "Comment"

    comment_id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("Post.post_id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("User.user_id"), primary_key=True)
    content: Mapped[LONGTEXT]
    timestamp: Mapped[datetime.datetime] = mapped_column(default=func.now())

    post: Mapped["Post"] = relationship(back_populates="user_comments")
    user: Mapped["User"] = relationship(back_populates="post_comments")
