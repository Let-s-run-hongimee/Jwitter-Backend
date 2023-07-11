from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.db.schemas import user_schema, tweet_schema
from app.db.models import tweet_model, user_model
from app.utils.hash import Hasher
from app.db.crud.read import get_user_by_login_id

async def add_to_db(db: Session, instance):
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance

async def create_user(db: Session, user: user_schema.UserCreate):
    # 유저네임 & 이메일 중복 확인
    existing_user = db.query(user_model.User).filter(
        or_(user_model.User.username == user.username, user_model.User.email == user.email)
    ).first()
    # 중복이 아니면 DB에 추가
    if not existing_user:
        hashed_password = Hasher.hashing(user.password)
        db_user = user_model.User(email=user.email, username=user.username, nickname=user.nickname, hashed_password=hashed_password)
        if await add_to_db(db, db_user):
            return db_user
    return False

        
async def add_refresh_token(db: Session, refresh_token: str, user_id: int):
    db_refresh_token = user_model.JwtToken(refresh_token=refresh_token, user_id=user_id)
    if await add_to_db(db, db_refresh_token):
        return True
    return False
    
    
async def create_tweet(db: Session, content: str, user_id: int):
    db_tweet = tweet_model.Tweet(content=content, author_id=user_id)
    if await add_to_db(db, db_tweet):
        return db_tweet
    return False

async def follow_user(db: Session, user_id: int, following_id: int):
    """
    User를 팔로우하는 함수
    
    Args:
        db (Session): DB Session
        user_id (int): 팔로우를 하는 유저의 user_id
        following_id (int): 팔로우를 당하는 유저의 user_id
        
    Returns:
        None
    """
    db_following = user_model.Followings(user_id=user_id, following_id=following_id)
    db_followers = user_model.Followers(user_id=following_id, follower_id=user_id)
    db.add(db_followers)
    db.add(db_following)
    db.commit()
    db.refresh(db_followers)
    db.refresh(db_following)
    return True