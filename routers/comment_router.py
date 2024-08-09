from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from typing import Annotated
import logging

from ..database import get_db
from ..schemas.comment_schemas import CommentOutput, CreateComment, EditComment
from ..services.comment_services import CommentService
from ..dependencies import *


router = APIRouter(
    prefix='/{post_id}/comments',
    tags=["Comments"]
)


@router.post("/new_comment", response_model=CommentOutput)
async def create(post_id: int, data: CreateComment, session: Session = Depends(get_db)):
    _service = CommentService(session)
    return _service.create(post_id, data)

@router.get("/all", response_model=list[CommentOutput])
async def get_all_post_comments(post_id: int, skip: int = 0, limit: int = 100, session: Session = Depends(get_db)):
    _service = CommentService(session)
    return _service.get_comments_under_post(post_id, skip, limit)

@router.get('/{comment_id}', response_model=CommentOutput)
async def get_comment(post_id: int, comment_id: int, session: Session = Depends(get_db)):
    _service = CommentService(session)
    return _service.get_comment(post_id, comment_id)

@router.put('/{comment_id}/edit', response_model=CommentOutput)
async def update(   post_id: int, comment_id: int, data: EditComment, session: Session = Depends(get_db),
                    user: UserOutput = Depends(get_current_user_post)):
    _service = CommentService(session)
    return _service.update(post_id, comment_id, data)

@router.delete('/{comment_id}/delete')
async def delete(   post_id: int, comment_id: int, session: Session = Depends(get_db),
                    user: UserOutput = Depends(get_current_user_post)):
    _service = CommentService(session)
    return _service.delete(post_id, comment_id, user.user_id)