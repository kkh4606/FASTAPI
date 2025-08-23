from pydantic import BaseModel, EmailStr, PlainSerializer

from datetime import datetime
from typing import Optional, List
from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(UserCreate):
    pass


class UserUpdate(UserCreate):
    pass


class PostOut(PostBase):
    id: int
    created_at: datetime
    votes: int = 0


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        form_attributes = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_tokne: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str | None] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)  # type:ignore
