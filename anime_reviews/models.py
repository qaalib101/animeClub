from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Review(models.Model):
    user = models.ForeignKey('auth.User', blank=False, on_delete=models.CASCADE)
    comments = models.TextField(max_length=300)
    posted_date = models.DateTimeField(auto_now_add=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True)
    positive_review = models.BooleanField()
    likes = models.IntegerField(blank=True, default=0)
    anime_id = models.IntegerField()
    anime_title = models.CharField(max_length=200)
    episode = models.IntegerField()
    season = models.IntegerField()

    def __str__(self):
        return f'Anime: {self.anime_title} Date posted: {self.posted_date}'

    def add_like(self):
        self.likes += 1
        self.save()

    def add_dislike(self):
        self.likes -= 1
        self.save()

class UserProfile(models.Model):
    user = models.ForeignKey('auth.User', blank=False, null=True, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)
    bio = models.TextField(null=True, blank=True)






