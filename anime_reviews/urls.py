from django.urls import path
from . import views, views_users, view_reviews

from django.contrib.auth import views as auth_views

app_name = 'anime_reviews'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('user/profile/<int:user_pk>/', views_users.user_profile, name='user_profile'),
    path('user/profile/', views_users.my_user_profile, name='my_user_profile'),
    path('user/profile/edit', views_users.edit_profile, name='edit_profile'),

    path('accounts/login/', views_users.login_and_signup, name='login_and_signup'),
    path('accounts/logout/', views_users.user_logout, name='logout'),
    path('register/', views_users.register, name='register'),

    path('anime/search/', view_reviews.search_anime, name='anime_search'),
    path('anime/detail/<int:anime_id>/', view_reviews.anime_detail, name='anime_detail'),

    path('reviews/new/<int:anime_id>/', view_reviews.new_review, name='new_review'),
    path('review/edit/<int:review_id>/', view_reviews.edit_review, name='edit_review'),
    path('review/delete/<int:review_id>/', view_reviews.delete_review, name='delete_review'),
    path('review/detail/<int:review_id>/', view_reviews.review_detail, name='review_detail'),
]