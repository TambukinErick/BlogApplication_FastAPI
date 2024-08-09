from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
import logging

from ..database import get_db
from ..schemas.interaction_schemas import InteractionOutput, CreateInteraction, InteractionType
from ..services.interaction_services import InteractionService
from ..dependencies import *


router = APIRouter(
    prefix="/{post_id}/interactions",
    tags=["Interactions"]
)
logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

@router.post('/new_interaction', response_model=InteractionOutput)
async def interact(post_id: int, data: CreateInteraction, session: Session = Depends(get_db),
                    user: UserOutput = Depends(get_current_user_post) ):
    _service = InteractionService(session)
    return _service.create(post_id, user.user_id, data)

@router.get('/all', response_model=list[InteractionOutput])
async def get_all_post_interactions(post_id, skip: int = 0, limit: int = 100, session: Session = Depends(get_db)):
    _service = InteractionService(session)
    return _service.get_all(post_id, skip, limit)

@router.get('/{interaction_type}', response_model=list[InteractionOutput])
async def get_all_by_interaction(post_id: int, interaction_type: InteractionType, 
                                skip: int = 0, limit: int = 100, 
                                session: Session = Depends(get_db)):
    _service = InteractionService(session)
    return _service.get_all_by_interaction(post_id, interaction_type, skip, limit)

@router.delete('/{interaction_id}/delete')
async def delete(post_id: int, interaction_id: int, session: Session = Depends(get_db),
                    user: UserOutput = Depends(get_current_user_post)):
    _service = InteractionService(session)
    return _service.delete(post_id, user.user_id, interaction_id)