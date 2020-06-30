from django.db import models
from datetime import datetime
# Create your models here.
class Users(models.Model):
    full_name = models.CharField(max_length=200, null = True)
    email = models.CharField(max_length=200, null = True)
    instagram = models.CharField(max_length=200, null = True)
    selfie = models.CharField(max_length=500, null = True)
    npi_score = models.IntegerField(default=0, null = True)
    biography = models.CharField(max_length=500, null = True, blank=True)
    media_count = models.IntegerField(default=0, null = True)
    followers = models.IntegerField(default=0, null = True)
    following = models.IntegerField(default=0, null = True)
    created_at = models.DateTimeField('created',default= datetime.now, null = True)
    state = models.TextField('state', default= 'pending')

class Posts(models.Model):
    user_id = models.BigIntegerField('user_id') #P.K
    instagram = models.CharField('instagram',max_length=200, null = True)  #F.K
    posted_on = models.DateTimeField('posted_on', null = True)
    post_url = models.TextField('post_url', null = True)
    hashtags = models.TextField('hashtags', null = True)
    mentions = models.TextField('mentions', null = True)
    tagged_users = models.TextField('tagged_users', null = True)
    is_video = models.BooleanField('is_video', default= False, null = True)
    likes = models.BigIntegerField('likes', null = True)
    caption = models.TextField('caption', null = True)

class Comment(models.Model):
    post_id = models.BigIntegerField('post_id', null = True)  # F.K
    posted_on = models.DateTimeField('posted_on', null = True)
    owner = models.CharField(max_length=200, null = True)
    is_comment = models.BooleanField('is_comment', null = True) #False if its a reply
    sentiment = models.CharField('sentiment', max_length=200, null = True)
    sscore = models.FloatField('sscore', null = True)
    tag_used = models.BooleanField ('tag_used', default= False, null = True) #True if the tag is used
    likes = models.IntegerField('likes', null = True)
    text = models.TextField('caption', null = True)

class Picture(models.Model):
    post_id = models.BigIntegerField('post_id', null = True)  # F.K
    instagram = models.CharField('instagram', max_length=200, null=True)  # F.K
    posted_on = models.DateTimeField('posted_on', null = True)
    selfie = models.BooleanField('selfie', default= False, null = True)  # True if the tag is used
    person = models.TextField('person', null = True) #include which person was identified
    image_path = models.TextField('image_path', null = True)

