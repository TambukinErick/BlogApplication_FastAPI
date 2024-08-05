import enum
import datetime
from typing import List
from sqlalchemy import String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .post_model import PostModel
from .comment_model import *
from .interaction_model import *
from ..database import Base

class UserModel(Base):
    __tablename__ = "User"

    user_id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    mobile: Mapped[str] = mapped_column(String(15), unique=True)
    registered_at: Mapped[datetime.datetime] = mapped_column(default=func.now())
    profile: Mapped[str] = mapped_column(LONGTEXT)
    disabled: Mapped[bool] = mapped_column(default=False)
    posts: Mapped[List["PostModel"]] = relationship(back_populates="user", cascade="all, delete", passive_deletes=True)

    post_comments: Mapped[List["CommentModel"]] = relationship(back_populates="user", 
                                                          cascade="all, delete", 
                                                          passive_deletes=True)
    
    post_interactions: Mapped[List["InteractionModel"]] = relationship(back_populates="user", 
                                                                  cascade="all, delete", 
                                                                  passive_deletes=True)