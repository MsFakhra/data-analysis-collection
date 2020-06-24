from django.db import models

# Create your models here.
class Users(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    instagram = models.CharField(max_length=200)
    selfie = models.CharField(max_length=500)
    npi_score = models.IntegerField(default=0)
    biography = models.CharField(max_length=500)
    media_count = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    created_at = models.DateTimeField('created')
    state = models.TextField('state', default= 'pending')

class Posts(models.Model):
    user_id = models.BigIntegerField('user_id') #P.K
    instagram = models.CharField('instagram',max_length=200)  #F.K
    posted_on = models.DateTimeField('posted_on')
    post_url = models.TextField('post_url')
    hashtags = models.TextField('hashtags')
    mentions = models.TextField('mentions')
    tagged_users = models.TextField('tagged_users')
    is_video = models.BooleanField('is_video', default= False)
    likes = models.BigIntegerField('likes')
    caption = models.TextField('caption')

class Comment(models.Model):
    post_id = models.BigIntegerField('post_id')  # F.K
    posted_on = models.DateTimeField('posted_on')
    owner = models.CharField(max_length=200)
    is_comment = models.BooleanField('is_comment') #False if its a reply
    sentiment = models.CharField('sentiment', max_length=200)
    sscore = models.FloatField('sscore')
    tag_used = models.BooleanField ('tag_used', default= False) #True if the tag is used
    likes = models.IntegerField('likes')
    caption = models.TextField('caption')

class Picture(models.Model):
    post_id = models.BigIntegerField('post_id')  # F.K
    posted_on = models.DateTimeField('posted_on')
    selfie = models.BooleanField('selfie', default= False)  # True if the tag is used
    person = models.TextField('person') #include which person was identified
    image_path = models.TextField('image_path')

