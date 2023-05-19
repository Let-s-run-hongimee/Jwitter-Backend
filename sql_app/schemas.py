from typing import List, Optional
from pydantic import BaseModel


class TweetBase(BaseModel):
    content: Optional[str] = None


class TweetCreate(TweetBase):
    content: str


class Tweet(TweetBase):
    tweetId: int
    userId: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    is_auth_user: Optional[bool] = None


class UserCreate(UserBase):
    username: str
    email: str
    password: str


class User(UserBase):
    userId: int
    tweets: List[Tweet] = []

    class Config:
        orm_mode = True


class PhotoBase(BaseModel):
    photoUrl: Optional[str] = None


class PhotoCreate(PhotoBase):
    photoUrl: str


class Photo(PhotoBase):
    photoId: int
    tweetId: int

    class Config:
        orm_mode = True
