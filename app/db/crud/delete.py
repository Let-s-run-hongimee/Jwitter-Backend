from sqlalchemy.orm import Session
from app.db.schemas import jwt_schema, user_schema, tweet_schema
from app.db.models import tweet_model, user_model
from app.utils.hash import Hasher
from app.db.crud.read import get_user_by_login_id

async def delete_refresh_token_by_userId(db: Session, user_id: int):
    existing_token = db.query(user_model.JwtToken).filter_by(user_id=user_id).first()
    if existing_token:
        db.delete(existing_token)
        db.commit()
        return True
    return False

async def delete_tweet(db: Session, tweet_id: int, user_id: int):
    existing_tweet = db.query(tweet_model.Tweet).filter_by(id=tweet_id).first()
    if existing_tweet:
        db.delete(existing_tweet)
        db.commit()
        return True
    return False

async def unfollow_user(db: Session, user_id: int, followed_user_id: int):
    """
    User를 언팔로우하는 함수 

    Args:
        db (Session): DB Session
        user_id (int): 언팔로우를 하는 유저의 user_id
        following_id (int): 언팔로우를 당하는 유저의 user_id
        
    Returns:
        None
    """
    
    # 두 테이블에서 각각 한개씩 데이터를 없애야함.(테이블 : user_model.Followings, user_model.Followers)
    # user_model.Followings 테이블에서 언팔로우를 하는 유저의 데이터를 찾아서 삭제
    existing_following = db.query(user_model.Followings).filter_by(user_id=user_id, following_id=followed_user_id).first()
    # user_model.Followers 테이블에서 언팔로우를 당하는 유저의 데이터를 찾아서 삭제
    existing_follower = db.query(user_model.Followers).filter_by(user_id=followed_user_id, follower_id=user_id).first()
    if existing_following and existing_follower:
        db.delete(existing_following)
        db.delete(existing_follower)
        db.commit()
        return True
    return False
