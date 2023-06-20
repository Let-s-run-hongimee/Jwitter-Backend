from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Tweet(Base):
    __tablename__ = "tweets"

    tweet_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    content = Column(String)
    
    photos = relationship("Photo", back_populates="tweet")
    user = relationship("User", back_populates="tweets")

class Photo(Base):
    __tablename__ = "photos"

    photo_id = Column(Integer, primary_key=True, index=True)
    tweet_id = Column(Integer, ForeignKey("tweets.tweet_id"))
    photoUrl = Column(String)

    tweet = relationship("Tweet", back_populates="photos")