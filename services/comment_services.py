from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..repositories.comment_repository import CommentRepository
from ..repositories.post_repository import PostRepository
from ..repositories.user_repository import UserRepository
from ..schemas.comment_schemas import CreateComment, CommentOutput, EditComment


class CommentService():
    def __init__(self, session: Session):
        self.comment_repository = CommentRepository(session)
        self.post_repository = PostRepository(session)
        self.user_repository = UserRepository(session)

    def create(self, post_id: int, data: CreateComment) -> CommentOutput:
        if post_id != data.post_id:
            raise HTTPException(status_code=404, datail="Post Path parameter does not match inputted data")
        if not self.user_repository.user_exists_by_id(data.user_id):
            raise HTTPException(status_code=404, detail="User does not exist")
        if not self.post_repository.post_exists(data.post_id):
            raise HTTPException(status_code=404, detail="Post does not exist")
        return self.comment_repository.create(data)
    
    def get_comments_under_post(self, post_id: int, skip: int = 0, limit: int = 100) -> List[CommentOutput]:
        if not self.post_repository.post_exists(post_id):
            raise HTTPException(status_code=404, detail="Post does not exist")
        return self.comment_repository.get_all_under_post(post_id, skip, limit)
    
    def get_comments_under_user(self, user_id: int, skip: int = 0, limit: int = 100) -> List[CommentOutput]:
        if not self.user_repository.user_exists_by_id(user_id):
            raise HTTPException(status_code=404, detail="User does not exist")
        return self.comment_repository.get_all_under_commenter(user_id, skip, limit)
    
    def get_comment(self, post_id: int, comment_id: int) -> CommentOutput:
        if not self.post_repository.post_exists(post_id):
            raise HTTPException(status_code=404, detail="Post does not exist")
        if not self.comment_repository.comment_exists(comment_id):
            raise HTTPException(status_code=404, detail="Comment does not exist")
        comment = self.comment_repository.get_comment(comment_id)
        return CommentOutput(**comment.__dict__)
    
    def update(self, post_id: int, comment_id: int, data: EditComment) -> CommentOutput:
        if not self.user_repository.user_exists_by_id(data.user_id):
            raise HTTPException(status_code=404, detail="User does not exist")
        if not self.post_repository.post_exists(post_id):
            raise HTTPException(status_code=404, detail="Post does not exist")
        if not self.comment_repository.comment_exists(comment_id):
            raise HTTPException(status_code=404, detail="Comment does not exist")
        comment = self.comment_repository.get_comment(comment_id)
        return self.comment_repository.update(comment, data)
    
    def delete(self, post_id: int, comment_id: int, user_id: int):
        if not self.user_repository.user_exists_by_id(user_id):
            raise HTTPException(status_code=404, detail="User does not exist")
        if not self.post_repository.post_exists(post_id):
            raise HTTPException(status_code=404, detail="Post does not exist")
        if not self.comment_repository.comment_exists(comment_id):
            raise HTTPException(status_code=404, detail="Comment does not exist")
        comment = self.comment_repository.get_comment(comment_id)
        return self.comment_repository.delete(comment)
