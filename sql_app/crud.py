from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
# hashing fuctions
from .utils import hashing

# ------------------ CRUD ------------------
# ※ Create ※

# Create API KEY
async def create_api_key(db: Session, key: str):
    decoded_key = str(str(datetime.now()) + "decoded_key" + key)
    hashed_key = hashing.hashing(key)
    db_key = models.APIKey(hashed_key=hashed_key)
    db.add(db_key)
    db.commit()
    db.refresh(db_key)
    return db_key

# Create User (Register)
async def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hashing.hashing(user.password)
    db_user = models.User(email=user.email, username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
# Create Tweet
async def create_tweet(db: Session, tweet: schemas.TweetCreate, user_id: int):
    if not tweet.content:
        return None
    db_tweet = models.Tweet(content=tweet.content, userId=user_id)
    db.add(db_tweet)
    db.commit()
    db.refresh(db_tweet)
    return db_tweet

# ※ Read ※

# has functions (return boolean)
async def is_username_taken(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return False
    return True

async def is_email_taken(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return False
    return True

async def is_api_key_valid(db: Session, key: str):
    db_key = db.query(models.APIKey).filter(models.APIKey.hashed_key == key).first()
    if not db_key:
        return False
    # Add additional checks here if necessary
    return True


# get functions (return data)

async def get_tweets(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Tweet).offset(skip).limit(limit).all()

async def get_tweets_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Tweet).filter(models.Tweet.userId == user_id).offset(skip).limit(limit).all()

async def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.userId == user_id).first()

async def get_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


# ※ UPDATE ※

# ※ DELETE ※



