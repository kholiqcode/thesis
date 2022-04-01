from datetime import datetime
import dateutil.parser
import json
import os
from core.classification import Classification
from classification.models import Account, Setting, Tweet
import tweepy as tw
from unidecode import unidecode
import pandas as pd

class Twitter(object):
    def __init__(self):
        self.TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
        self.TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
        self.TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
        self.TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        self.auth = tw.OAuthHandler(self.TWITTER_CONSUMER_KEY,
                                    self.TWITTER_CONSUMER_SECRET)
        self.auth.set_access_token(self.TWITTER_ACCESS_TOKEN,
                                   self.TWITTER_ACCESS_TOKEN_SECRET)
        self.api = tw.API(self.auth, wait_on_rate_limit=True)

    def search(self, username,total=200):
        tweets = self.api.search_tweets(q="to:"+username,lang="id",count=total,tweet_mode="extended")
        # with open('readme.txt', 'w') as f:
        #     f.write(str(tweets))
        #     return
        # Strips the newline character
        setting = Setting.objects.filter(id=1).first()
        classification = Classification(test_size=setting.model_type)
        for item in tweets:
            try:
                sentiment = classification.predict(unidecode(item.full_text))

                data = {
                    'uids': item.id,
                    'username': str(item.user.screen_name),
                    'name': unidecode(item.user.name),
                    'profile_id': str(item.user.id_str),
                    'created_at': None if item.created_at == '' else pd.to_datetime(item.created_at),
                    'tweet': unidecode(item.full_text),
                    'mention_to':username,
                    'sentiment': sentiment,
                }
                obj, created  = Tweet.objects.update_or_create(
                    uids = data['uids'],
                    defaults=data
                )
            except Exception as e:
                print(e)
                print(e.args)
                print(e.with_traceback)
                # raise e


    def account(self,username):
        user = self.api.get_user(screen_name=username)

        data = {
            'profile_id' : user.id_str,
            'username' : str(user.screen_name),
            'name' : unidecode(str(user.name)),
            'location' : unidecode(str(user.location)),
            'description' : unidecode(str(user.description)),
            'likes_count' : user.favourites_count,
            'retweets_count' : user.listed_count,
            'followers_count' : user.followers_count,
            'friends_count' : user.friends_count,
            'statuses_count' : user.statuses_count,
            'verified' : user.verified,
            'profile_background_image_url' : user.profile_background_image_url_https,
            'profile_banner_url' : None if user.profile_banner_url is None else user.profile_banner_url,
            'profile_image_url' : user.profile_image_url_https,
            'created_at' : datetime.strptime(str(user.created_at), "%Y-%m-%d %H:%M:%S%z"),
        }
        try:
            obj, created  = Account.objects.update_or_create(
                username = user.screen_name,
                defaults=data
            )
            return data
        except Exception as e:
            print(e)
            return {}

