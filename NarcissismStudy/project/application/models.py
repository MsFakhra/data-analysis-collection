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

class Posts(models.Model):
    postid = models.BigIntegerField(primary_key=True)
    instagram = models.CharField(max_length=200)
    url = models.TextField()
    hashtags = models.TextField()