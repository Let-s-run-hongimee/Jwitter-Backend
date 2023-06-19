from sqlalchemy.orm import Session
from app.db.schemas import jwt_schema, user_schema, tweet_schema
from app.db.models import tweet_model, user_model
from app.utils.hash import Hasher
from app.db.crud.read import get_user_by_login_id

# Delete Refresh Token using user id
async def delete_refresh_token_by_userId(db: Session, user_id: int):
    existing_token = db.query(user_model.JwtToken).filter_by(user_id=user_id).first()
        
    # If it does, delete it
    if existing_token:
        db.delete(existing_token)
        db.commit()
        return True
    return False