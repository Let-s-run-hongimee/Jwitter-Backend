from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.schemas import tweet_schema, user_schema
from app.db.crud import create, read, update, delete, the_algorithm
from app.utils.jwt import JWT
from typing import List, Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

router = APIRouter()

@router.get("/foryou", response_model=List[tweet_schema.TweetResponse])
async def read_for_you_tweets(db: Session = Depends(get_db), token: Annotated[str, Depends(oauth2_scheme)] = None, skip: int = 0, limit: int = 10):
    subject = JWT.verify_token_and_get_sub(token)
    tweets = the_algorithm.algorithm_1(db, subject, skip, limit)
    if not tweets:
        raise HTTPException(status_code=404, detail="No tweets found")
    return tweets

@router.get("/me", response_model=List[tweet_schema.TweetResponse])
async def read_user_tweets(db: Session = Depends(get_db), token: Annotated[str, Depends(oauth2_scheme)] = None, skip: int = 0, limit: int = 10):
    subject = JWT.verify_token_and_get_sub(token)
    tweets = read.get_tweets_from_user_id(db, subject, skip, limit)
    if not tweets:
        raise HTTPException(status_code=404, detail="No tweets found")
    return tweets

@router.post("/create")
async def create_tweet(tweet: tweet_schema.TweetCreate, db: Session = Depends(get_db), token: Annotated[str, Depends(oauth2_scheme)] = None):
    subject = JWT.verify_token_and_get_sub(token)
    tweet_db = await create.create_tweet(db, tweet.content, subject)

    if not tweet_db:
        raise HTTPException(status_code=404, detail="Tweet not created")
    return {
        "id" : tweet_db.id,
        "username" : tweet_db.user.username,
        "nickname" : tweet_db.user.nickname,
        "content" : tweet_db.content
    }

@router.put("/update")
async def update_tweet(tweet: tweet_schema.TweetUpdate, db: Session = Depends(get_db), token: Annotated[str, Depends(oauth2_scheme)] = None):
    subject = JWT.verify_token_and_get_sub(token)

    if await update.update_tweet(db, tweet, subject):
        raise HTTPException(status_code=200, detail="Tweet updated")
    raise HTTPException(status_code=404, detail="Tweet not Found")
    

@router.delete("/delete")
async def delete_tweet(tweet_id: int, db: Session = Depends(get_db), token: Annotated[str, Depends(oauth2_scheme)] = None):
    subject = JWT.verify_token_and_get_sub(token)

    if await delete.delete_tweet(db, tweet_id, subject):
        raise HTTPException(status_code=200, detail="Tweet deleted")
    raise HTTPException(status_code=404, detail="Tweet not Found")

