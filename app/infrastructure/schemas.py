from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr


class UserIn(UserBase):
    password: str


class UserCreate(UserIn):
    username: str


class UserInDB(UserBase):
    hashed_password: str| None = None
    username: str
    is_active: bool = True
    is_admin: bool = False

    class Config:
        from_attributes = True


class UserItem(UserBase):
    user_id: int
    username: str
    email: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access: str
    refresh: str


class TokenPayload(BaseModel):
    sub: int | None = None
    token_type: str


class BookBase(BaseModel):
    name: str
    author: str
    image: str | None = None
    isbn: str | None = None

    class Config:
        from_attributes = True

