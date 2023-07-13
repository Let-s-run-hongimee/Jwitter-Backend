from sqlalchemy.orm import Session
from app.db.schemas import user_schema, tweet_schema
from app.db.models import tweet_model, user_model
from app.utils.hash import Hasher
from sqlalchemy import or_
from app.the_algorithm.ai.ai import linear_regression
from app.db.crud.read import count_hearts_and_retweets
import numpy as np
from app.db.crud import create, read, update, delete

class TheAlgorithm:

    def has_link(tweet_text: str):
        """
        트윗에 링크가 포함되어있는지 확인하는 함수
        """
        return True if 'http' in tweet_text else False
    
    def has_media_link(tweet_text: str):
        """
        트윗에 미디어(이미지, 동영상) 링크가 포함되어있는지 확인하는 함수
        """
        return True if 'pic.twitter.com' in tweet_text else False
    
    def has_news_link(tweet_text: str):
        """
        트윗에 뉴스 링크가 포함되어있는지 확인하는 함수
        """
        return True if 'news' in tweet_text else False

    def calculate_not_spam_score(predicted_likes):
        # 10% 이상부터 100%까지의 비율과 점수를 정의합니다.
        thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        scores = list(range(1, len(thresholds) + 1))

        # 예측된 비율을 계산합니다.
        ratio = predicted_likes * 0.1

        # 비율에 따른 점수 계산
        for threshold, score in zip(thresholds, scores):
            if ratio >= threshold:
                not_spam_score = score
            else:
                break

        return not_spam_score

    async def SpamVectorScoring(db: Session, user_id: int):
        #팔로잉 되어있는 사람들의 트윗 가져옴
        tweets_db = (
            db.query(tweet_model.Tweet)
            .join(user_model.Follow, user_model.Follow.followed_id == tweet_model.Tweet.author_id)
            .filter(user_model.Follow.follower_id == user_id)
            .all()
        )

        # 트윗을 한번씩 방문
        Data = VectorScoringDataClass()
        tweets: list = []
        
        for tweet in tweets_db:
            if tweet.user.is_auth_user:
                continue
            # 트윗의 텍스트를 가져옴
            tweet_text = tweet.content
            # 트윗에 링크가 포함되어있고, 미디어(이미지, 동영상) 및 뉴스 링크가 아닌 경우
            if TheAlgorithm.has_link(tweet_text) and not TheAlgorithm.has_media_link(tweet_text) and not TheAlgorithm.has_news_link(tweet_text):
                Data.NOT_SPAM_SCORE += 1
            else:
                Data.SPAM_SCORE += 2
            # 트윗의 참여 횟수(좋아요)가 선형회귀 모델값의 10퍼센트 이상인 경우
            follower_count = await read.get_follower_count(db, tweet.author_id)
            following_count = await read.get_following_count(db, tweet.author_id)
            retweet_count = read.count_retweet(db, tweet.id)
            
            predicted_likes = linear_regression(retweet_count, follower_count, following_count)
            Data.NOT_SPAM_SCORE = TheAlgorithm.calculate_not_spam_score(predicted_likes)
            
            # 트윗의 참여 횟수(좋아요)가 선형회귀 모델값의 10퍼센트 미만인 경우
            Data.SPAM_SCORE = 10 - Data.NOT_SPAM_SCORE

            # 트윗의 작성자가 팔로우한 사람들의 수가 100명 또는 1000명 이상인 경우
            if following_count >= 100 or following_count >= 1000:
                Data.NOT_SPAM_SCORE += 1
            else:
                Data.SPAM_SCORE += 1
            # 트윗 작성자의 팔로워 수가 100명 또는 1000명 이상인 경우
            if follower_count >= 100 or follower_count >= 1000:
                Data.NOT_SPAM_SCORE += 1
            else:
                Data.SPAM_SCORE += 1

            # 스팸이 아니면
            if Data.NOT_SPAM_SCORE > Data.SPAM_SCORE:
                tweets.append(tweet)
        return tweets

        

    @staticmethod
    async def Finish_algorithm(db: Session, user_id: int):
        popularity_score = 0
        tweets = await TheAlgorithm.SpamVectorScoring(db, user_id)

        for index, tweet in enumerate(tweets):
            follower_count = await read.get_follower_count(db, tweet.author_id)
            following_count = await read.get_following_count(db, tweet.author_id)
            retweet_count = read.count_retweet(db, tweet.id)
            heart_count = read.count_heart(db, tweet.id)

            predicted_likes = linear_regression(retweet_count, follower_count, following_count)
            actual_likes = np.array([heart_count])
            errors = actual_likes - predicted_likes
            errors_value = np.min(errors)
            for count, i in enumerate(range(0, 500, 50)):
                if errors_value > 0:
                    if errors_value > i:
                        # Assign popularity score directly to the tweet
                        popularity_score = i / count + 1
                    break

        # Sort the tweets by popularity score
        tweets_sorted = sorted(tweets, key=lambda x: popularity_score, reverse=True)

        # Return the top 10 tweets
        return tweets_sorted[:10]

        

class VectorScoringDataClass:
    # SpamVectorScoring

    IS_SPAM: bool = False

    SPAM_TWEET_INDEX: list[int] = []
    NOT_SPAM_SCORE: int = 0 # 스팸이 아닌 점수
    SPAM_SCORE: int = 0

