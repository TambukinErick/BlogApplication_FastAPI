from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..models.post_model import PostModel
from ..schemas.post_schemas import *
from typing import List, Optional, Type


class PostRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: CreatePost) -> PostOutput:
        post = PostModel(**data.model_dump(exclude_none=True))
        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)
        return PostOutput(**post.__dict__)
    
    def get_all_by_user(self, author_id: int, skip: int, limit: int) -> List[Optional[PostOutput]]:
        posts = (self.session.query(PostModel)
                 .filter_by(author_id = author_id).offset(skip).limit(limit).all())
        return [PostOutput(**post.__dict__) for post in posts]
    
    def get_all_by_category(self, category: str, skip: int, limit: int) -> List[Optional[PostOutput]]:
        posts = (self.session.query(PostModel).filter(PostModel.category == category)
                .offset(skip).limit(limit).all())
        return [PostOutput(**post.__dict__) for post in posts]
    
    def get_all_by_category_by_user(self, author_id: int, category: str,
                            skip: int, limit: int) -> List[Optional[PostOutput]]:
        posts = (self.session.query(PostModel).filter(
                and_(PostModel.author_id == author_id, PostModel.category == category))
                .offset(skip).limit(limit).all())
        return [PostOutput(**post.__dict__) for post in posts]
    
    def get_post(self, post_id: int) -> PostModel:
        post = self.session.query(PostModel).filter_by(post_id = post_id).first()
        return post
    
    def post_exists(self, post_id: int) -> bool:
        post = self.session.query(PostModel).filter_by(post_id = post_id).first()
        return bool(post)
    
    def update(self, post: type[PostModel], data: UpdatePost) -> PostOutput:
        for key, value in data.model_dump(exclude_none=False).items():
            setattr(post, key, value)
        self.session.commit()
        self.session.refresh(post)
        return PostOutput(**post.__dict__)
    
    def delete(self, post: type[PostModel]):
        self.session.delete(post)
        self.session.commit()
        return {"Message": "Post Deleted"}