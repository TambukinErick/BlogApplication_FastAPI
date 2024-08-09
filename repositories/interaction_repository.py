from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..models.interaction_model import InteractionModel
from ..schemas.interaction_schemas import InteractionOutput, InteractionType, CreateInteraction
from typing import List, Optional, Type

class InteractionRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, data: CreateInteraction) -> InteractionOutput:
        interaction = InteractionModel(**data.model_dump(exclude_none=False))
        self.session.add(interaction)
        self.session.commit()
        self.session.refresh(interaction)
        return InteractionOutput(**interaction.__dict__)
    
    def intraction_exists(self, interaction_id: int):
        interaction = self.session.query(InteractionModel).filter_by(interaction_id = interaction_id).first()
        return bool(interaction)
    
    def get_interaction(self, interaction_id: int):
        interaction = self.session.query(InteractionModel).filter_by(interaction_id = interaction_id).first()
        return interaction
    
    def get_all(self, post_id: int, skip: int, limit: int) -> List[Optional[InteractionOutput]]:
        interactions = self.session.query(InteractionModel).filter_by(post_id = post_id).offset(skip).limit(limit).all()
        return [InteractionOutput(**interaction.__dict__) for interaction in interactions]
    
    def get_by_interaction(self, post_id: int, interaction_type: str, skip: int, limit: int) -> List[Optional[InteractionOutput]]:
        interactions = self.session.query(InteractionModel).filter( and_(
                                                                        InteractionModel.post_id == post_id, 
                                                                        InteractionModel.interaction_type == interaction_type)
                                                                    ).offset(skip).limit(limit).all()
        return [InteractionOutput(**interaction.__dict__) for interaction in interactions]
    
    def delete(self, interaction: Type[InteractionModel]):
        self.session.delete(interaction)
        self.session.commit()
        return {"Message": "Interaction Deleted"}
