from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
import datetime


class InteractionType(str, Enum):
    Like = "Like"
    Share = "Share"
    Bookmark = "Bookmark"

class CreateInteraction(BaseModel):
    post_id: int
    user_id: int
    interaction_type: InteractionType = InteractionType.Like

class InteractionOutput(CreateInteraction):
    interaction_id: int
    timestamp: datetime.datetime
