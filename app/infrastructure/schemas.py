from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    username: str
    password: str


class UserItem(UserBase):
    user_id: int
    username: str
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True
