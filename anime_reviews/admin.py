from django.contrib import admin
from .models import Review, Announcement, UserProfile
# Register your models here.

admin.site.register(Review)
admin.site.register(Announcement)