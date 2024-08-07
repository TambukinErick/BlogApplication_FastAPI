from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .utils import (
    ALGORITHM,
    SECRET_KEY
)
import jwt
from pydantic import ValidationError
from .schemas.user_schemas import UserOutput
from .schemas.token_schema import TokenSchema, TokenPayload
from .database import get_db
from .repositories.user_repository import UserRepository

import logging


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/users/login",
    scheme_name="JWT"
)

class UserOAuth2PasswordBearer(OAuth2PasswordBearer):
    pass
class PostOAuth2PasswordBearer(OAuth2PasswordBearer):
    pass
class CommentOAuth2PasswordBearer(OAuth2PasswordBearer):
    pass
class InteractionOAuth2PasswordBearer(OAuth2PasswordBearer):
    pass

oauth2_scheme_user = UserOAuth2PasswordBearer(tokenUrl="/users/login", scheme_name="JWT")
def get_current_user_user(token: str = Depends(oauth2_scheme_user), session: Session = Depends(get_db)) -> UserOutput:
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    _repository = UserRepository(session)
    user = _repository.get_user(token_data.sub)
    
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    
    return UserOutput(**user.__dict__)


oauth2_scheme_post = UserOAuth2PasswordBearer(tokenUrl="/posts/login", scheme_name="JWT")
def get_current_user_post(token: str = Depends(oauth2_scheme_post), session: Session = Depends(get_db)) -> UserOutput:
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    _repository = UserRepository(session)
    user = _repository.get_user(token_data.sub)
    
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    
    return UserOutput(**user.__dict__)


oauth2_scheme_comment = UserOAuth2PasswordBearer(tokenUrl="/comment/login", scheme_name="JWT")
def get_current_user_comment(token: str = Depends(oauth2_scheme_comment), session: Session = Depends(get_db)) -> UserOutput:
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    _repository = UserRepository(session)
    user = _repository.get_user(token_data.sub)
    
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    
    return UserOutput(**user.__dict__)


oauth2_scheme_interaction = UserOAuth2PasswordBearer(tokenUrl="/interaction/login", scheme_name="JWT")
def get_current_user_interaction(token: str = Depends(oauth2_scheme_interaction), session: Session = Depends(get_db)) -> UserOutput:
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    _repository = UserRepository(session)
    user = _repository.get_user(token_data.sub)
    
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    
    return UserOutput(**user.__dict__)