from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from typing import List

from ..repositories.post_repository import PostRepository
from ..repositories.user_repository import UserRepository
from ..schemas.token_schema import Token, TokenData
from ..schemas.post_schemas import CreatePost, PublishedPost, UpdatePost, PostOutput, PostCategory


class PostService:
    def __init__(self, session: Session):
        self.post_repository = PostRepository(session)
        self.user_repository = UserRepository(session)

    def create(self, data: CreatePost):
        return self.post_repository.create(data)
    
    def get_all(self, username: str, skip: int, limit: int):
        if not self.user_repository.user_exists_by_username(username):
            raise HTTPException(status_code=404, details="User doesnt exist")
        user_id = self.user_repository.get_user_id(username) 
        return self.post_repository.get_all_by_user(user_id, skip, limit)
    
    def get_post(self, post_id) -> PostOutput:
        if not self.post_repository.post_exists(post_id):
            raise HTTPException(status_code=404, details="Post doesnt exist")
        post = self.post_repository.get_post(post_id)
        return PostOutput(**post.__dict__)
    
    def get_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[PostOutput]:
         if category not in PostCategory:
             raise HTTPException(status_code=404, detail="Category does not exist")
         return self.post_repository.get_all_by_category(category, skip, limit)
    
    def get_by_user_and_filter_by_category(self, username: str, category: str, 
                                           skip: int = 0, limit: int = 100) -> List[PostOutput]:
        if not self.user_repository.user_exists_by_username(username):
            raise HTTPException(status_code=404, detail="User doesnt exist")
        if category not in PostCategory:
            raise HTTPException(status_code=404, detail="Category does not exist")
        
        user = self.user_repository.get_by_username(username)
        return self.post_repository.get_all_by_category_by_user(user.user_id, category, skip, limit)
    
    def update(self, data: UpdatePost) -> PostOutput:
        if not self.post_repository.post_exists(data.post_id):
            raise HTTPException(status_code=404, detail="Post doesnt exist")
        post = self.post_repository.get_post(data.post_id)
        updated_post = self.post_repository.update(post, data)

        return updated_post
    
    def delete(self, post_id: int):
        if not self.post_repository.post_exists(post_id):
            raise HTTPException(status_code=404, detail="Post doesnt exist")
        post = self.post_repository.get_post(post_id)
        return self.post_repository.delete(post)
        