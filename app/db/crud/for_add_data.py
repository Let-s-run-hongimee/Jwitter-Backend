from sqlalchemy.orm import Session
from app.db.models import tweet_model, user_model
import random
from typing import List

def create_user(db: Session, username: str, email: str, nickname: str, hashed_password: str):
    db_user = user_model.User(username=username, email=email, nickname=nickname, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_tweet(db: Session, user_id: int, content: str):
    db_tweet = tweet_model.Tweet(author_id=user_id, content=content)
    db.add(db_tweet)
    db.commit()
    db.refresh(db_tweet)
    return db_tweet

def create_heart(db: Session, user_id: int, tweet_id: int):
    db_heart = tweet_model.Heart(user_id=user_id, tweet_id=tweet_id)
    db.add(db_heart)
    db.commit()
    db.refresh(db_heart)
    return db_heart

def create_retweet(db: Session, user_id: int, tweet_id: int):
    db_retweet = tweet_model.Retweet(user_id=user_id, tweet_id=tweet_id)
    db.add(db_retweet)
    db.commit()
    db.refresh(db_retweet)
    return db_retweet

def create_follow(db: Session, follower_id: int, followed_id: int):
    db_follow = user_model.Follow(follower_id=follower_id, followed_id=followed_id)
    db.add(db_follow)
    db.commit()
    db.refresh(db_follow)
    return db_follow

def generate_user_data(db: Session, n_users: int):
    usernames = ["User" + str(i) for i in range(n_users)]
    emails = ["user" + str(i) + "@example.com" for i in range(n_users)]
    nicknames = ["Nickname" + str(i) for i in range(n_users)]
    hashed_passwords = ["Password" + str(i) for i in range(n_users)]
    users = [create_user(db, username, email, nickname, hashed_password) for username, email, nickname, hashed_password in zip(usernames, emails, nicknames, hashed_passwords)]
    
    for user in users:
        n_tweets = random.randint(0, 20)
        for _ in range(n_tweets):
            content = "Tweet content " + str(random.randint(0, 10000))
            tweet = create_tweet(db, user.id, content)
            
            n_hearts = random.randint(0, 10)
            for _ in range(n_hearts):
                heart_user_id = random.choice(users).id
                create_heart(db, heart_user_id, tweet.id)
            
            n_retweets = random.randint(0, 5)
            for _ in range(n_retweets):
                retweet_user_id = random.choice(users).id
                create_retweet(db, retweet_user_id, tweet.id)
        
        n_followers = random.randint(0, 10)
        for _ in range(n_followers):
            follower_id = random.choice(users).id
            if follower_id != user.id:
                create_follow(db, follower_id, user.id)
        
        n_following = random.randint(0, 10)
        for _ in range(n_following):
            followed_id = random.choice(users).id
            if followed_id != user.id:
                create_follow(db, user.id, followed_id)
