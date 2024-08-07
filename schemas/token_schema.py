from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

class TokenData(BaseModel):
    username: str | None = None

class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None