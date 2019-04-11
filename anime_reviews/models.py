from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Review(models.Model):
    user = models.ForeignKey('auth.User', blank=False, on_delete=models.CASCADE)
    comments = models.CharField(max_length=300)
    posted_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    positive_review = models.BooleanField()
    anime_name = models.CharField(max_length=200)
    episode = models.CharField(max_length=200)
    aired_date = models.DateField()


class UserProfile(models.Model):
    user = models.ForeignKey('auth.User', blank=False, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)






