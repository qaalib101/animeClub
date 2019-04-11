from django.urls import path
from . import views, views_users

from django.contrib.auth import views as auth_views

app_name = 'anime_reviews'

urlpatterns = [
    path('', views.homepage, name='homepage'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LoginView.as_view(template_name='registration/logout.html'), name='logout'),
    path('register/', views_users.register, name='register'),
]