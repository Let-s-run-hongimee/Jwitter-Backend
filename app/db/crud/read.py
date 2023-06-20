from sqlalchemy.orm import Session
from app.db.schemas import jwt_schema, user_schema, tweet_schema
from app.db.models import tweet_model, user_model
from app.utils.hash import Hasher
from sqlalchemy import or_

async def get_user_by_login_id(db: Session, login_id: str):
    """
    username 또는 email로 User를 DB에서 찾는 함수
    
    Args:
        db (Session): DB Session
        login_id (str): username or email value
            
    Returns:
        user (User): User Model
        None (NoneType): if user is not found
    """
    user = db.query(user_model.User).filter(
        or_(user_model.User.username == login_id, user_model.User.email == login_id)
    ).first()
    if user:
        return user
    return False

async def login_verify(db: Session, user: user_schema.UserLogin):
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

async def get_user_tweets(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(tweet_model.Tweet)
        .filter(tweet_model.Tweet.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )