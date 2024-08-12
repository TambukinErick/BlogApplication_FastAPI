from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
import datetime

class PostCategory(str, Enum):
    Fashion = "Fashion" 
    Music = "Music" 
    DIY = "DIY" 
    Parenting = "Parenting" 
    Movies = "Movies"
    Pets = "Pets" 
    Photography = "Photography" 
    Food = "Food" 
    Lifestyle = "Lifestyle" 
    Sports = "Sports"
    Business = "Business" 
    Cars = "Cars" 
    VideoGames = "Video Games" 
    Travel = "Travel" 
    Fitness = "Fitness"
    Finance = "Finance" 
    Personal = "Personal" 
    News = "News" 
    Affiliate = "Affiliate" 
    Misc = "Misc"


class CreatePost(BaseModel):
    author_id: int
    title: str
    content: str
    category: PostCategory
    creation_date: datetime.datetime

class PublishedPost(CreatePost):
    publication_date: Optional[datetime.datetime] = None

class PostOutput(CreatePost):
    post_id: int
    publication_date: Optional[datetime.datetime] = None
    update_at: Optional[datetime.datetime] = None
    interactions: Optional[int] = Field(default=0)
    comments: Optional[int] = Field(default=0)


class UpdatePost(PublishedPost):
    post_id: int
    update_at: Optional[datetime.datetime]
    updated: bool = Field(default=True)

