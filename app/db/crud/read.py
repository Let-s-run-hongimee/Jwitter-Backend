from sqlalchemy.orm import Session
from app.db.schemas import user_schema
from app.db.models import tweet_model, user_model
from app.utils.hash import Hasher
from sqlalchemy import or_

async def get_user_by_login_id(db: Session, login_id: str):
    """
    username 또는 email로 User를 DB에서 찾는 함수
    """
    user = db.query(user_model.User).filter(
        or_(user_model.User.username == login_id, user_model.User.email == login_id)
    ).first()
    if user:
        return user
    return False

async def verify_refresh_token(db: Session, token: str, user_id: int):
    """
    refresh token이 유효한지 확인하는 함수
    """
    token_db = db.query(user_model.JwtToken).filter_by(refresh_token=token).first()
    if token_db and token_db.user_id == user_id:
        return True
    return False

async def verify_user(db: Session, user: user_schema.UserLogin):
    db_user = await get_user_by_login_id(db, user.id)
    if db_user:
        if Hasher.verify_hashed_text(plain_password=user.password, hashed_text=db_user.hashed_password):
            return db_user
    return False

async def get_user_by_user_id(db: Session, user_id: int):
    user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if user:
        return user
    return False

async def get_tweets_from_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(tweet_model.Tweet)
        .filter(tweet_model.Tweet.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

async def is_following(db: Session, following_id: int, user_id: int):
    return{
        db.query(user_model.Followings)
        .filter(user_model.Followings.following_id == following_id)
        .filter(user_model.Followings.user_id == user_id)
        .first()
    }

async def is_followed(db: Session, following_id: int, user_id: int):
    return{
        db.query(user_model.Followings)
        .filter(user_model.Followings.following_id == user_id)
        .filter(user_model.Followings.user_id == following_id)
        .first()
    }