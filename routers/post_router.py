from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from typing import Annotated
import logging

from ..database import get_db
from ..schemas.post_schemas import PostOutput, CreatePost, UpdatePost, PublishedPost, PostCategory
from ..services.post_services import PostService
from ..dependencies import *


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.post('/create')
async def create_post(post: CreatePost, session: Session = Depends(get_db), 
                     user: UserOutput = Depends(get_current_user_post)):
    _service = PostService(session)
    return _service.create(post)

@router.get("/{username}/articles", response_model=list[PostOutput])
async def read_posts(username: str, skip: int = 0, limit: int = 100, session: Session = Depends(get_db)):
    _service = PostService(session)
    return _service.get_all(username, skip, limit)

@router.get("/{post_id}/articles", response_model=PostOutput)
async def read_post(post_id: int, session: Session = Depends(get_db)):
    _service = PostService(session)
    return _service.get_post(post_id)

@router.get("/all_articles", response_model=list[PostOutput])
async def read_post_by_category(category: PostCategory, skip: int = 0, limit: int = 100, session: Session = Depends(get_db)):
    _service = PostService(session)
    return _service.get_by_category(category, skip, limit)

@router.put("/{post_id}/edit", response_model=PostOutput)
async def edit_post(data: UpdatePost, session: Session = Depends(get_db), user: UserOutput = Depends(get_current_user_post)):
    _service = PostService(session)
    return _service.update(data)

@router.delete("/{post_id}/delete")
async def delete(post_id: int, session: Session = Depends(get_db), user: UserOutput = Depends(get_current_user_post)):
    _service = PostService(session)
    return _service.delete(post_id)

