from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from typing import List, Annotated

from ..repositories.user_repository import UserRepository
from ..schemas.token_schema import Token, TokenData
from ..schemas.user_schemas import *
from ..utils import get_hashed_password, verify_password
import logging
class UserService:
    def __init__(self, session: Session) -> None:
        self.user_repo = UserRepository(session)

    def authenticate_user(self, email: str, password: str):
        if not self.user_repo.user_exists(email):
           return False
        user = self.user_repo.get_user(email)
        if not verify_password(password, user.password):
            return False
        return RegisterUser(**user.__dict__)

    def register_user(self, data: RegisterUser):
        if self.user_repo.user_exists(data.email):
            raise HTTPException(status_code=400, detail="User account already exists")
        hashed_password = get_hashed_password(data.password)

        data.password = hashed_password
        return self.user_repo.create(data)
    
    def get_user(self, email: str):
        if self.user_repo.user_exists(email):
            raise HTTPException(status_code=400, detail="User account already exists")
        return self.user_repo.get_user(email)

    def get_user_by_username(self, username: str):
        if self.user_repo.user_exists_by_username(username):
            user = self.user_repo.get_by_username(username)
            return UserOutput(**user.__dict__)
        raise HTTPException(status_code=400, detail="User doesnt exist")
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[UserOutput]:
        return self.user_repo.get_all(skip, limit)
    
    def update(self, data: UpdateUser, user_token: UserOutput):
        if not self.user_repo.user_exists(data.email):
            raise HTTPException(status_code=404, detail="User not found")
        if (data.username == user_token.username) and (data.email == user_token.email):
            user = self.user_repo.get_by_username(data.username)
            updated_user = self.user_repo.update(user, data)
            return updated_user
    
    def delete(self, data: DeleteUser, user: UserOutput):
        if not self.user_repo.user_exists(data.email):
            raise HTTPException(status_code=404, detail="User not found")
        if data.email != user.email:
            raise HTTPException(status_code=404, detail="Wrong account being deleted")
        user = self.user_repo.get_user(data.email)
        if not verify_password(data.password, user.password):
            return False
        self.user_repo.delete(user)
    


    
