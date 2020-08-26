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
    private = models.BooleanField('isprivate',default= False)
    # Seven Components https://psychcentral.com/cgi-bin/narcissisticquiz.cgi
    authority = models.IntegerField(default=0, null = True) # Authority refers to a person's leadership skills and power. People who score higher on authority like to be in charge and gain power, often for power's sake alone.
    sufficiency = models.IntegerField(default=0, null = True)  # This trait refers to how self-sufficient a person is, that is, how much you rely on others versus your own abilities to meet your needs in life.
    superior = models.IntegerField(default=0, null = True)  # This trait refers to whether a person feels they are more superior than those around them.
    exhibit = models.IntegerField(default=0, null = True)  # This trait refers to a person's need to be the center of attention, and willingness to ensure they are the center of attention (even at the expense of others' needs).
    exploit = models.IntegerField(default=0, null = True)  # This trait refers to how willing you are to exploit others in order to meet your own needs or goals.
    vanity = models.IntegerField(default=0, null = True)  # This trait refers to a person's vanity, or their belief in one's own superior abilities and attractiveness compared to others.
    entitle = models.IntegerField(default=0, null = True)  # This trait refers to the expectation and amount of entitlement a person has in their lives, that is, unreasonable expectations of especially favorable treatment or automatic compliance with one's expectations. People who score higher on this trait generally have a greater expectation of entitlement, while those who score lower expect little from others or life.


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

class Follow(models.Model):
    recorded_at = models.DateTimeField('recorded_at',default= datetime.now, null = True)
    followers = models.BigIntegerField('followers', null = True)
    following = models.BigIntegerField('following', null = True)
    instagram = models.CharField(max_length=200, null = True)
