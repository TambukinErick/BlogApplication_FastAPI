from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..models.comment_model import CommentModel
from ..schemas.comment_schemas import CreateComment, CommentOutput, EditComment
from typing import List, Optional, Type

class CommentRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: CreateComment) -> CommentOutput:
        comment = CommentModel(**data.model_dump(exclude_none=False))
        self.session.add(comment)
        self.session.commit()
        self.session.refresh(comment)
        return CommentOutput(**comment.__dict__)

    def get_comment(self, comment_id):
        return self.session.query(CommentModel).filter_by(comment_id = comment_id).first()
    
    def get_all_under_post(self, post_id: int, skip: int, limit: int) -> List[Optional[CommentOutput]]:
        comments = self.session.query(CommentModel).filter_by(post_id = post_id).offset(skip).limit(limit).all()
        return [CommentOutput(**comment.__dict__) for comment in comments]
    
    def get_all_under_commenter(self, user_id: int, skip: int, limit: int) -> List[Optional[CommentOutput]]:
        comments = self.session.query(CommentModel).filter_by(user_id = user_id).offset(skip).limit(limit).all()
        return [CommentOutput(**comment.__dict__) for comment in comments]

    def comment_exists(self, comment_id: int) -> bool:
        comment = self.session.query(CommentModel).filter_by(comment_id = comment_id).first()
        return bool(comment)
    
    def update(self, comment: Type[CommentModel], data: EditComment) -> CommentOutput:
        for key, value in data.model_dump(exclude_none=False).items():
            setattr(comment, key, value)
        self.session.commit()
        self.session.refresh(comment)
        return CommentOutput(**comment.__dict__)
    
    def delete(self, comment: Type[CommentModel]):
        self.session.delete(comment)
        self.session.commit()
        return {"Message": "Comment Deleted"}
