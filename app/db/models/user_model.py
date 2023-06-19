from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_auth_user = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    tweets = relationship("Tweet", back_populates="user")
    jwttokens = relationship("JwtToken", back_populates="user")
    
class JwtToken(Base):
    __tablename__ = "jwttokens"

    jwttoken_id = Column(Integer, primary_key=True, index=True)
    refresh_token = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True, index=True)

    user = relationship("User", back_populates="jwttokens")