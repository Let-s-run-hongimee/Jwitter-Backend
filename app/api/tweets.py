from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.schemas import tweet_schema, user_schema
from app.db.crud import create, read, update, delete
from fastapi_jwt_auth import AuthJWT
from typing import List

router = APIRouter()

@router.get("/me", response_model=List[tweet_schema.TweetResponse])
async def read_user_tweets(request: Request, db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    Authorize: AuthJWT = request.state.auth # Load AuthJWT
    Authorize.jwt_required()

    current_uesr = Authorize.get_jwt_subject()
    tweets = read.get_user_tweets(db, current_uesr, skip, limit)
    if not tweets:
        raise HTTPException(status_code=404, detail="No tweets found")
    return tweets

@router.post("/create")
async def create_tweet(request: Request, tweet: tweet_schema.TweetCreate, db: Session = Depends(get_db)):
    Authorize: AuthJWT = request.state.auth # Load AuthJWT
    Authorize.jwt_required()
    current_uesr = Authorize.get_jwt_subject()

    data = await create.create_tweet(db, tweet, current_uesr)
    if not data:
        raise HTTPException(status_code=404, detail="Tweet not created")
    return {
        "username" : data.username,
        "content" : data.content
    }