from enum import Enum
from django.db import models
from django.forms import model_to_dict

# Create your models here.
class ModelType(Enum):

    SATU = 1
    DUA = 2
    TIGA = 3
    EMPAT = 4

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class Setting(models.Model):
    model_type = models.SmallIntegerField(null=True, choices=ModelType.choices(),default=ModelType.DUA)
    threshold_min = models.SmallIntegerField(null=True,default=1)
    threshold_max = models.SmallIntegerField(null=True)
    accuracy_score = models.FloatField(null=True)
    confusion_matrix = models.FloatField(null=True)
    precision_score = models.JSONField(null=True)
    recall_score = models.JSONField(null=True)
    f1_score = models.JSONField(null=True)
    is_active = models.BooleanField(null=True,default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        db_table = 'settings'

    def get_accuracy_score(self):
        if self.accuracy_score == int(self.accuracy_score):
            self.accuracy_score = int(self.accuracy_score)
        return self.accuracy_score

class Account(models.Model):
    profile_id = models.CharField(max_length=100,null=True)
    username = models.CharField(max_length=100,null=True)
    name = models.CharField(max_length=100,null=True)
    location = models.CharField(max_length=100,null=True)
    description = models.CharField(max_length=255,null=True)
    likes_count = models.IntegerField(null=True)
    retweets_count = models.IntegerField(null=True)
    likes_count = models.IntegerField(null=True)
    followers_count = models.IntegerField(null=True)
    friends_count = models.IntegerField(null=True)
    statuses_count = models.IntegerField(null=True)
    verified = models.BooleanField(null=True,default=False)
    profile_image_url = models.CharField(max_length=255,null=True)
    profile_banner_url = models.CharField(max_length=255,null=True)
    profile_background_image_url = models.CharField(max_length=255,null=True)
    score = models.FloatField(null=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        db_table = 'accounts'
    
    def to_dict(self):
        data = model_to_dict(self)
        return data
    def first(self):
        return self[0]

class Tweet(models.Model):
    uids = models.CharField(max_length=100)
    profile_id = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    geo = models.CharField(max_length=20,null=True)
    likes_count = models.IntegerField(null=True)
    retweets_count = models.IntegerField(null=True)
    hashtags = models.JSONField(null=True)
    conversation_id = models.CharField(max_length=100,null=True)
    urls = models.JSONField(null=True)
    mentions = models.JSONField(null=True)
    tweet = models.TextField()
    timezone = models.CharField(max_length=20,null=True)
    place = models.CharField(max_length=100,null=True)
    photos = models.JSONField(null=True)
    replies_count = models.IntegerField(null=True)
    retweets_count = models.IntegerField(null=True)
    cashtags = models.JSONField(null=True)
    link = models.CharField(max_length=100,null=True)
    retweet = models.BooleanField(null=True,default=False)
    quote_url = models.CharField(max_length=100,null=True)
    video = models.IntegerField(null=True)
    user_rt_id = models.CharField(max_length=100,null=True)
    near = models.CharField(max_length=100,null=True)
    source = models.CharField(max_length=100,null=True)
    retweet_date = models.DateTimeField(null=True)
    reply_to = models.JSONField(null=True)
    mention_to = models.CharField(max_length=100,null=True)
    sentiment = models.CharField(null=True,max_length=20)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        db_table = 'tweets'
    def to_dict(self):
        data = model_to_dict(self)
        return data