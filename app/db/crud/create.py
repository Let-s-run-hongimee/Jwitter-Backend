from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.db.schemas import jwt_schema, user_schema, tweet_schema
from app.db.models import tweet_model, user_model
from app.utils.hash import Hasher
from app.db.crud.read import get_user_by_login_id

async def add_to_db(db: Session, instance):
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance

async def create_user(db: Session, user: user_schema.UserCreate):
    """
    User를 DB에 추가하는 비동기 함수 (회원가입)
    
        Args:
            db (Session): DB Session
            user (UserCreate): UserCreate Schema
            
        Returns:
            db_user (user_model.User): if user is created
            None (NoneType): if username or email already exists
    """
    # 유저네임 & 이메일 중복 확인
    existing_user = db.query(user_model.User).filter(
        or_(user_model.User.username == user.username, user_model.User.email == user.email)
    ).first()
    # 중복이 아니면 DB에 추가
    if not existing_user:
        hashed_password = Hasher.hashing(user.password)
        db_user = user_model.User(email=user.email, username=user.username, hashed_password=hashed_password)
        return await add_to_db(db, db_user)
    return False

        
async def add_refresh_token(db: Session, refresh_token: str, user_id: int):
    """
    User의 Refresh Token을 DB에 추가하는 함수
    
        Args:
            db (Session): DB Session
            refresh_token (str): Refresh Token
            
        Retruns:
            None
    """
    db_refresh_token = user_model.JwtToken(refresh_token=refresh_token, user_id=user_id)
    await add_to_db(db, db_refresh_token)
    
async def create_tweet(db: Session, tweet: tweet_schema.TweetCreate, login_id: str):
    """
    Tweet을 DB에 추가하는 함수
    
    Args:
        db (Session): DB Session
        tweet (TweetCreate): TweetCreate Schema
        login_id (str): username or email value

    Returns:
        db_tweet (Tweet): Tweet Model
        None (NoneType): if user is not found
    """
    if not tweet.content:
        return None
    user = await get_user_by_login_id(db, login_id)
    if user:
        db_tweet = tweet_model.Tweet(content=tweet.content, userId=user.user_id)
        return await add_to_db(db, db_tweet)
    return None