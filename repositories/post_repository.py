from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, select, func, desc, text

from ..models.post_model import PostModel
from ..models.interaction_model import InteractionModel
from ..schemas.post_schemas import *
from typing import List, Optional, Type
import logging

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
        posts = self.session.scalars(select(PostModel).filter_by(author_id = author_id).offset(skip).limit(limit)).all()
        return [PostOutput(**post.__dict__) for post in posts]
    
    def get_all_by_category(self, category: str, skip: int, limit: int) -> List[Optional[PostOutput]]:
        posts = self.session.scalars(select(PostModel).filter(PostModel.category == category).offset(skip).limit(limit)).all()
        return [PostOutput(**post.__dict__) for post in posts]
    
    def get_all_by_category_by_user(self, author_id: int, category: str,
                            skip: int, limit: int) -> List[Optional[PostOutput]]:

        posts = self.session.scalars(select(PostModel).filter(
            and_(PostModel.author_id == author_id, PostModel.category == category)
            ).offset(skip).limit(limit)).all()
        return [PostOutput(**post.__dict__) for post in posts]
    
    def get_post(self, post_id: int) -> PostModel:
        post = self.session.query(PostModel).filter_by(post_id = post_id).first()
        return post
    
    def get_by_interactions(self):
        sql = text("""SELECT posts.*, count(interactions.post_id) as num_of_interactions 
                   FROM Post as posts 
                   LEFT JOIN Interaction as interactions 
                   ON (posts.post_id = interactions.post_id) 
                   group by posts.post_id;""")
        results = self.session.execute(sql)
        output = []
        for result in results:
            temp_post_output = PostOutput(
                post_id = result[0],
                author_id = result[1],
                title = result[2],
                content = result[3],
                category = result[4],
                creation_date = result[5],
                publication_date = result[6],
                update_at = result[7],
                interactions = result[8]
            )
            output.append(temp_post_output)
        return output
    
    def get_by_comments(self):
        sql = text("""SELECT posts.*, count(comments.post_id) as num_of_comments 
                   FROM Post as posts 
                   LEFT JOIN Comment as comments 
                   ON (posts.post_id = comments.post_id) 
                   group by posts.post_id;""")
        results = self.session.execute(sql)
        output = []
        for result in results:
            temp_post_output = PostOutput(
                post_id = result[0],
                author_id = result[1],
                title = result[2],
                content = result[3],
                category = result[4],
                creation_date = result[5],
                publication_date = result[6],
                update_at = result[7],
                comments = result[8]
            )
            output.append(temp_post_output)
        return output

    def get_by_publish_date(self, publish_date, skip: int, limit: int) -> List[Optional[PostOutput]]:
        posts = self.session.query(PostModel).filter_by(publication_date=publish_date).offset(skip).limit(limit).all()
        return [PostOutput(**post.__dict__) for post in posts]
    
    def get_by_date_range(self, start_date, end_date, skip: int, limit: int) -> List[Optional[PostOutput]]:
        posts = self.session.query(PostModel).filter(and_(
            PostModel.publication_date <= end_date, PostModel.publication_date >= start_date
        )).offset(skip).limit(limit).all()
        return [PostOutput(**post.__dict__) for post in posts]

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