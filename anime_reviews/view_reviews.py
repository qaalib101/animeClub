from django.shortcuts import render, redirect
from jikanpy import Jikan, JikanException
from .models import Review
from .forms import UserRegistrationForm, UserLoginForm, AnimeSearchForm, ReviewForm
from django.conf import settings
from datetime import datetime
import requests
import requests_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


requests_cache.install_cache()
@login_required
def search_anime(request):
    form = AnimeSearchForm()
    if request.method == 'POST':
        form = AnimeSearchForm(request.POST)
        search = form['anime_search'].value()
        if search != None:
            payload = {'q': search, 'page': '1'}
            r = requests.get('https://api.jikan.moe/v3/search/anime', params=payload).json()
            try:
                result = r['results']
                return render(request, 'anime_reviews/reviews/anime_search.html', {'form': form, 'shows': result})
            except :
                message = 'No show by that name found'
                return render(request, 'anime_reviews/reviews/anime_search.html', {'form': form, 'message': message})
        else:
            message = 'Enter a anime to search'
            return render(request, 'anime_reviews/reviews/anime_search.html', {'form': form, 'message': message})
    else:
        reviews = Review.objects.all().order_by('posted_date', 'likes').reverse()
        return render(request, 'anime_reviews/reviews/anime_search.html', {'form': form, 'reviews': reviews})


@login_required
def anime_detail(request, anime_id):
    show = requests.get(f'https://api.jikan.moe/v3/anime/{anime_id}').json()
    if 'error' in show.keys():
        form = AnimeSearchForm()
        message = f'{anime_id} is not a correct id for an anime.'
        return render(request, 'anime_reviews/reviews/anime_search.html', {'form': form, 'message': message})
    else:
        reviews = Review.objects.filter(anime_id=anime_id).order_by('posted_date', 'likes').reverse()
        return render(request, 'anime_reviews/reviews/anime_detail.html', {'show': show, 'reviews': reviews})

@login_required
def new_review(request, anime_id):
    show = requests.get(f'https://api.jikan.moe/v3/anime/{anime_id}').json()
    if 'error' in show.keys():
        form = AnimeSearchForm()
        message = f'{anime_id} is not a correct id for an anime.'
        return render(request, 'anime_reviews/reviews/anime_search.html', {'form': form, 'message': message})
    else:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.anime_id = anime_id
                review.anime_title = show['title']
                review.posted_date = datetime.now()
                review.save()
                return redirect('anime_reviews:review_detail', review_id=review.id)
            else:
                message = "Enter correct information"
                return render(request, 'anime_reviews/reviews/new_review.html', {'form': form, 'show': show, 'message': message})
        else:
            form = ReviewForm()
            return render(request, 'anime_reviews/reviews/new_review.html', {'form': form, 'show': show})
@login_required
def edit_review(request, review_id):
    instance = Review.objects.get(id=review_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
        return render(request, 'anime_reviews/reviews/review_detail.html')
    else:
        form = ReviewForm(instance=instance)
        return render(request, 'anime_reviews/reviews/edit_review.html', {'form': form, 'show': instance})
@login_required
def review_detail(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
        return render(request, 'anime_reviews/reviews/review_detail.html', {'review': review})
    except Review.DoesNotExist:
        return render(request, 'anime_reviews/home.html')
@login_required
def delete_review(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
        if request.user == review.user:
            Review.objects.get(id=review_id).delete()
        return render(request, 'anime_reviews/reviews/review_detail.html', {'review': review})
    except Review.DoesNotExist:
        return render(request, 'anime_reviews/home.html')
