from django.shortcuts import render, redirect
from jikanpy import Jikan, JikanException
from .models import Review
from .forms import UserRegistrationForm, UserLoginForm, AnimeSearchForm
from django.conf import settings
import requests
import requests_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

jikan = Jikan()
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
        result = []
        return render(request, 'anime_reviews/reviews/anime_search.html', {'form': form})


def anime_detail(request, anime_id):
    r = requests.get(f'https://api.jikan.moe/v3/anime/{anime_id}').json()
    return render(request, 'anime_reviews/reviews/anime_detail.html', {'show': r})
