from sqlalchemy.orm import Session
from . import models, schemas
from .utils import hashing


# Create User (Register)
async def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hashing.hashing(user.password)
    db_user = models.User(email=user.email, username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
# Create Tweet
async def create_tweet(db: Session, tweet: schemas.TweetCreate, login_id: str):
    if not tweet.content:
        return None
    user_id = await get_userid_by_login(db, login_id)
    db_tweet = models.Tweet(content=tweet.content, userId=user_id)
    db.add(db_tweet)
    db.commit()
    db.refresh(db_tweet)
    return db_tweet


async def login_verify(db: Session, user: schemas.UserLogin):
    data = await is_username_taken(db, user.id)
    if not data:
        data = await is_email_taken(db, user.id)
        if not data:
            return False
    return hashing.verify_hashing(user.password, data.hashed_password)
    
async def is_username_taken(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        return user
    return False

async def is_email_taken(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        return user
    return False

async def get_userid_by_login(db: Session, login_id: str):
    user = await is_username_taken(db, login_id)
    if not user:
        user = await is_email_taken(db, login_id)
        if not user:
            return False
    return user.user_id

async def get_all_tweets(db: Session, login_id: str):
    user_id = await get_userid_by_login(db, login_id)
    tweets = db.query(models.Tweet).filter(models.Tweet.userId == user_id).all()
    return tweets