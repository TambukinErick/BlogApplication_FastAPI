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
        print(data.password)
        return self.user_repo.create(data)
    
    def get_user(self, email: str):
        if self.user_repo.user_exists(email):
            raise HTTPException(status_code=400, detail="User account already exists")
        return self.user_repo.get_user(email)



    
