from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from typing import Annotated
import logging

from ..database import get_db
from ..schemas.post_schemas import PostOutput, CreatePost, UpdatePost, PublishedPost, PostCategory
from ..services.post_services import PostService
from ..dependencies import *
from ..utils import create_access_token, create_refresh_token


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.post('/create')
async def create_post(post: CreatePost, session: Session = Depends(get_db), 
                     user: UserOutput = Depends(get_current_user_post)):
    _service = PostService(session)
    return _service.create(post)

@router.get("/view_posts/{username}", response_model=list[PostOutput])
async def read_posts(username: str, skip: int = 0, limit: int = 100, session: Session = Depends(get_db)):
    _service = PostService(session)
    return _service.get_all(username, skip, limit)

@router.get("/read_post/{post_id}", response_model=PostOutput)
async def read_post(post_id: int, session: Session = Depends(get_db)):
    _service = PostService(session)
    return _service.get_post(post_id)

@router.get("/view_posts", response_model=list[PostOutput])
async def read_post_by_category(category: PostCategory, skip: int = 0, limit: int = 100, session: Session = Depends(get_db)):
    _service = PostService(session)
    return _service.get_by_category(category, skip, limit)

@router.put("/edit/{", response_model=PostOutput)
async def edit_post(data: UpdatePost, session: Session = Depends(get_db), user: UserOutput = Depends(get_current_user_post)):
    _service = PostService(session)
    return _service.update(data)

@router.delete("/delete/{post_id}")
async def delete(post_id: int, session: Session = Depends(get_db), user: UserOutput = Depends(get_current_user_post)):
    _service = PostService(session)
    return _service.delete(post_id)

