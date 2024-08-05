import enum
import datetime
from typing import Optional, List, Literal, get_args
from sqlalchemy import ForeignKey, String, DateTime, Enum
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from ..database import Base

class UserModel(Base):
    __tablename__ = "User"

    user_id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    mobile: Mapped[str] = mapped_column(String(15), unique=True)
    registered_at: Mapped[datetime.datetime] = mapped_column(default=func.now())
    profile: Mapped[LONGTEXT]

    posts: Mapped[List["Post"]] = relationship(back_populates="user", cascade="all, delete", passive_deletes=True)

    post_comments: Mapped[List["Comment"]] = relationship(back_populates="user")
    
    post_interactions: Mapped[List["Interaction"]] = relationship(back_populates="user")