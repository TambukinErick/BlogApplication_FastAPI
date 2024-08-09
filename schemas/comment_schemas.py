from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
import datetime

class CreateComment(BaseModel):
    post_id: int
    user_id: int
    content: str
    timestamp: datetime.datetime

class CommentOutput(CreateComment):
    comment_id: int
    timestamp: datetime.datetime

class EditComment(BaseModel):
    comment_id: int
    post_id: int
    user_id: int
    content: str