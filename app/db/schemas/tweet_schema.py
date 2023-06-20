from pydantic import BaseModel
from typing import Optional, List

# Tweet related schemas
class TweetBase(BaseModel):
    content: Optional[str] = None

class TweetCreate(TweetBase):
    pass

class Tweet(TweetBase):
    tweet_id: int
    user_id: int
    username: str

    class Config:
        orm_mode = True

class TweetResponse(TweetBase):
    tweets: List[Tweet] = []