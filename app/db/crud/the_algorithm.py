from sqlalchemy.orm import Session
from app.db.schemas import jwt_schema, user_schema, tweet_schema
from app.db.models import tweet_model, user_model
from app.utils.hash import Hasher
from sqlalchemy import or_