from datetime import datetime
from typing import Annotated

from fastapi import UploadFile, Form
from pydantic import BaseModel, EmailStr, Field, FilePath


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


class Tokens(BaseModel):
    access: str
    refresh: str


class TokenPayload(BaseModel):
    sub: int | None = None
    exp: datetime | None = None
    token_type: str


class BookBase(BaseModel):
    name: str = Form(...)
    author: str = Form(...)
    image: str | None = None
    isbn: str | None = None

    class Config:
        from_attributes = True


class UserBookIn(BaseModel):
    user: UserItem
    book: BookBase
    is_read: bool = False
