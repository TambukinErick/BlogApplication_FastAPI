import enum
import datetime
from typing import Optional, List, Literal, get_args
from sqlalchemy import ForeignKey, String, DateTime, Enum
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from ..database import Base

InteractionType = Literal["Like", "Share", "Bookmark"]

class InteractionModel(Base):
    __tablename__ = "Interaction"

    interaction_id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("Post.post_id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("User.user_id"), primary_key=True)
    interaction_type: Mapped[InteractionType] = mapped_column(Enum(*get_args(InteractionType),
        name="interaction_type",
        create_constraint=True,
        validate_strings=True,
    ), nullable=False)
    timestamp: Mapped[datetime.datetime] = mapped_column(default=func.now())

    post: Mapped["Post"] = relationship(back_populates="user_interactions")
    user: Mapped["User"] = relationship(back_populates="post_interactions")