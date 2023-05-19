from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    userId = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_auth_user = Column(Boolean, default=False)

    tweets = relationship("Tweet", back_populates="user")

class Tweet(Base):
    __tablename__ = "tweets"

    tweetId = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    userId = Column(Integer, ForeignKey("users.userid"))

    user = relationship("User", back_populates="tweets")

class Photo(Base):
    __tablename__ = "photos"

    photoId = Column(Integer, primary_key=True, index=True)
    tweetId = Column(Integer, ForeignKey("tweets.tweetid"))
    photoUrl = Column(String)

    tweet = relationship("Tweet", back_populates="photos")