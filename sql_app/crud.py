from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
# hashing fuctions
from .utils import hashing
#
import secrets
# ------------------ CRUD ------------------
# ※ Create ※

# Create API KEY
async def create_api_key(db: Session, userData: schemas.UserAdminVerify):
    user = db.query(models.User).filter(models.User.username == userData.username).first()
    if user:
        if user.email == userData.email and hashing.verify_hashing(userData.password, user.hashed_password):
            if user.is_admin:
                api_key = generate_api_key(db, user)
                return api_key
    return False


def generate_api_key(db: Session, user: models.User):
    api_key = secrets.token_hex(20)
    hashed_key = hashing.hashing(api_key)
    # delete old key
    db.query(models.APIKey).filter(models.APIKey.userId == user.user_id).delete()
    db.commit()
    # create new key
    db_key = models.APIKey(hashed_key=hashed_key, userId=user.user_id)
    db.add(db_key)
    db.commit()
    db.refresh(db_key)
    return api_key


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
async def get_userid_by_username(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return None
    return user.user_id

async def login_verify(db: Session, user: schemas.UserLogin):
    data = db.query(models.User).filter(models.User.username == user.id).first()
    if not data:
        data = db.query(models.User).filter(models.User.email == user.id).first()
        if not data:
            return False
    return hashing.verify_hashing(user.password, data.hashed_password)
    






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

async def is_api_key_valid(db: Session, key: str, username: str):
    # get api key
    data = db.query(models.APIKey).join(models.User).filter(models.User.username == username).first()
    # check if key is valid
    if hashing.verify_hashing(key, data.hashed_key):
        return True
    return False


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



