from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..models.user_model import UserModel
from ..schemas.user_schemas import RegisterUser, UserOutput, UpdateUser
from typing import List, Optional, Type

class UserRepository:
    def __init__(self, session: Session):
        self.session = session
        
    def create(self, data: RegisterUser):
        user = UserModel(**data.model_dump(exclude_none=True))
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return {"message":"user created successfully"}

    def get_all(self, skip: int, limit: int) -> List[Optional[UserOutput]]:
        users =  self.session.query(UserModel).offset(skip).limit(limit).all()
        return [UserOutput(**user.__dict__) for user in users]

    def get_user(self, email: str):
        return self.session.query(UserModel).filter_by(email = email).first()
    
    def get_by_username(self, username: str):
        return self.session.query(UserModel).filter_by(username = username).first()
        
    def user_exists(self, email: str) -> bool:
        user = self.session.query(UserModel).filter_by(email = email).first()
        return bool(user)
    
    def user_exists_by_username(self, username: str) -> bool:
        user = self.session.query(UserModel).filter_by(username = username).first()
        return bool(user)

    def update(self, user: Type[UserModel], data: UpdateUser) -> UserOutput:
        for key, value in data.model_dump(exclude_none=False).items():
            setattr(user, key, value)
        self.session.commit()
        self.session.refresh(user)
        return UserOutput(**user.__dict__)
    

    def delete(self, user: Type[UserModel]) -> bool:
        self.session.delete(user)
        self.session.commit()
        return True





