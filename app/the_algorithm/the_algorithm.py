from sqlalchemy.orm import Session
from app.db.schemas import user_schema, tweet_schema
from app.db.models import tweet_model, user_model
from app.utils.hash import Hasher
from sqlalchemy import or_


async def algorithm_1(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    """
    
    """