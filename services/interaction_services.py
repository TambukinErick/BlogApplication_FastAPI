from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

from ..repositories.interaction_repository import InteractionRepository
from ..repositories.post_repository import PostRepository
from ..repositories.user_repository import UserRepository
from ..schemas.interaction_schemas import CreateInteraction, InteractionOutput, InteractionType


class InteractionService:
    def __init__(self, session: Session):
        self.interaction_repository = InteractionRepository(session)
        self.post_repository = PostRepository(session)
        self.user_repository = UserRepository(session)

    def create(self, post_id: int, user_id: int, data: CreateInteraction) -> InteractionOutput:
        if user_id != data.user_id:
            raise HTTPException(status_code=404, detail="Conflicting User ids")
        if self.user_repository.user_exists_by_id(user_id) == False:
            raise HTTPException(status_code=404, detail="User Doesnt Exist")
        if not self.post_repository.post_exists(post_id):
            raise HTTPException(status_code=404, detail="Post Doesnt Exist")
        return self.interaction_repository.create(data)
    
    def get_all(self, post_id, skip: int, limit: int) -> List[InteractionOutput]:
        if not self.post_repository.post_exists(post_id):
            raise HTTPException(status_code=404, detail="Post Doesnt Exist")
        return self.interaction_repository.get_all(post_id, skip, limit)
    
    def get_all_by_interaction(self, post_id, interaction_type: str, skip: int, limit: int) -> List[InteractionOutput]:
        if not self.post_repository.post_exists(post_id):
            raise HTTPException(status_code=404, detail="Post Doesnt Exist")
        return self.interaction_repository.get_by_interaction(post_id, interaction_type, skip, limit)
    
    def delete(self, post_id, user_id, interaction_id):
        if not self.user_repository.user_exists_by_id(user_id):
            raise HTTPException(status_code=404, detail="User Doesnt Exist")
        if not self.post_repository.post_exists(post_id):
            raise HTTPException(status_code=404, detail="Post Doesnt Exist")
        if not self.interaction_repository.intraction_exists(interaction_id):
            raise HTTPException(status_code=404, detail="Interaction Doesnt Exist")

        interaction = self.interaction_repository.get_interaction(interaction_id)
        return self.interaction_repository.delete(interaction)
