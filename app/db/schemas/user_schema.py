from pydantic import BaseModel
from typing import Optional

# User related schemas
class UserBase(BaseModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    user_id: int

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    id: str
    password: str
