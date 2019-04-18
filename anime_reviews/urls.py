from django.urls import path
from . import views, views_users

from django.contrib.auth import views as auth_views

app_name = 'anime_reviews'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('user/profile/<int:user_pk>/', views_users.user_profile, name='user_profile'),
    path('user/profile/', views_users.my_user_profile, name='my_user_profile'),

    path('accounts/login/', views_users.login_and_signup, name='login_and_signup'),
    path('accounts/logout/', auth_views.LoginView.as_view(template_name='registration/logout.html'), name='logout'),
    path('register/', views_users.register, name='register'),
]