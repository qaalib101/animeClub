from django.shortcuts import render

# Create your views here.

def homepage(request):
    return render(request, 'anime_reviews/home.html')
