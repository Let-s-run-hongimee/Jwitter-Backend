from pydantic import BaseModel
from typing import Optional, List

# Tweet related schemas

class TweetUpdate(BaseModel):
    tweet_id: int
    content: Optional[str] = None

class TweetCreate(BaseModel):
    content: Optional[str] = None

class Tweet(BaseModel):
    tweet_id: int
    user_id: int
    username: str
    content: Optional[str] = None
    heart: int
    retweet: int

    class Config:
        orm_mode = True

class TweetResponse(BaseModel):
    tweets: List[Tweet]