from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from enum import Enum
import datetime

class RegisterUser(BaseModel):
    username: str
    password: str
    email: EmailStr
    mobile: str
    registered_at: datetime.datetime
    profile: str
    disabled: bool = Field(default=False)

class UserOutput(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    mobile: str
    registered_at: datetime.datetime
    profile: str
    disabled: bool

class UpdateUser(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    mobile: str
    profile: str

class SystemUser(BaseModel):
    user_id: int
    email: str
    password: str


class DeleteUser(BaseModel):
    email: str
    password: str
