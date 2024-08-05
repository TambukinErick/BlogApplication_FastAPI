import enum
import datetime
from typing import Optional, List, Literal, get_args
from sqlalchemy import ForeignKey, String, Enum
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from ..database import Base

PostCategory = Literal["Fashion", "Music", "DIY", "Parenting", "Movies",
                       "Pets", "Photography", "Food", "Lifestyle", "Sports",
                       "Business", "Cars", "Video Games", "Travel", "Fitness"
                       "Finance", "Personal", "News", "Affiliate", "Misc"
                       ]

class PostModel(Base):
    __tablename__ = "Post"

    post_id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("User.user_id"), ondelete="CASCADE")
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[LONGTEXT]
    category: Mapped[PostCategory] = mapped_column(Enum(*get_args(PostCategory),
        name="post_category",
        create_constraint=True,
        validate_strings=True,
    ), nullable=False)
    creation_date: Mapped[datetime.datetime] = mapped_column(default=func.now())
    publication_date: Mapped[Optional[datetime.datetime]]
    update_at: Mapped[Optional[datetime.datetime]]
    updated: Mapped[bool] = mapped_column(default=False)

    user: Mapped["User"] = relationship(back_populates="posts")

    user_comments: Mapped[List["User"]] = relationship(back_populates="post")

    user_interactions: Mapped[List["Interaction"]] = relationship(back_populates="post")
