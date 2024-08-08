from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from typing import Annotated
import logging

from ..database import get_db
from ..schemas.user_schemas import UserOutput, RegisterUser, UpdateUser, DeleteUser
from ..services.user_services import UserService
from ..dependencies import *
from ..utils import create_access_token, create_refresh_token



router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/login")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
                                 session: Session = Depends(get_db)):
    # logger = logging.getLogger('uvicorn.error')
    # logger.setLevel(logging.DEBUG)
    # logger.debug("Hello")
    _service = UserService(session)
    user = _service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},)
    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email)
    }

@router.post("/register")
async def register_user(user: RegisterUser, session: Session = Depends(get_db)):
    _service = UserService(session)
    return _service.register_user(user)

@router.get("/token/profile", summary='Get details of currently logged in user')
async def get_me(user: UserOutput = Depends(get_current_user_user)):
    return user

@router.get("/token/users", response_model=list[UserOutput])
async def read_users(skip: int = 0, limit: int = 100, session: Session = Depends(get_db), 
                     user: UserOutput = Depends(get_current_user_user)):
    _service = UserService(session)
    return _service.get_all(skip, limit)

@router.get("/token/{username}", response_model=UserOutput)
async def read_user(username: str, session: Session = Depends(get_db), 
                    user: UserOutput = Depends(get_current_user_user)):
    _service = UserService(session)
    return _service.get_user_by_username(username)

@router.put("/token/update_profile")
async def update_profile(data: UpdateUser, session: Session = Depends(get_db), 
                         user: UserOutput = Depends(get_current_user_user)):
    _service = UserService(session)
    return _service.update(data, user)

@router.delete("/token/delete")
async def delete_account(data: DeleteUser, session: Session = Depends(get_db), 
                         user: UserOutput = Depends(get_current_user_user)):
    _service = UserService(session)
    return _service.delete(data, user)







