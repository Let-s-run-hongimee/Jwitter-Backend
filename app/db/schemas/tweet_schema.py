from pydantic import BaseModel
from typing import Optional

# Tweet related schemas
class TweetBase(BaseModel):
    content: Optional[str] = None

class TweetCreate(TweetBase):
    pass

class Tweet(TweetBase):
    tweet_id: int
    user_id: int

    class Config:
        orm_mode = True
