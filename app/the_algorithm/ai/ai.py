import pickle
import numpy as np

def linear_regression(retweet_count, follower_count, following_count):
    # 저장된 모델을 불러옵니다.
    model = pickle.load(open('app/the_algorithm/ai/twitter_linear_regression_model.pkl', 'rb'))

    # 예측하려는 데이터를 준비합니다.
    # 이 경우에는 retweets=5000, followers=10000, following=200으로 가정합니다.
    data = np.array([[retweet_count, follower_count, following_count]])

    # 모델을 사용하여 예측합니다.
    predicted_likes = model.predict(data)
    
    return predicted_likes[0]