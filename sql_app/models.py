from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_auth_user = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    tweets = relationship("Tweet", back_populates="user")

class Tweet(Base):
    __tablename__ = "tweets"

    tweet_id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    userId = Column(Integer, ForeignKey("users.user_id"))
    
    photos = relationship("Photo", back_populates="tweet")
    user = relationship("User", back_populates="tweets")

class Photo(Base):
    __tablename__ = "photos"

    photo_id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(Integer, ForeignKey("tweets.tweet_id"))
    photoUrl = Column(String)

    tweet = relationship("Tweet", back_populates="photos")