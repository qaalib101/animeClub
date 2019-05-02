from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import Http404
import os
from .models import Review, UserProfile, Announcement
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def user_profile(request, user_pk):
    user = User.objects.get(pk=user_pk)
    reviews = Review.objects.all().filter(user=user_pk).order_by('posted_date').reverse()
    try:
        profile = UserProfile.objects.get(user=user.pk)
        return render(request, 'users/user_profile.html', {'user': user, 'reviews': reviews, 'profile': profile})
    except UserProfile.DoesNotExist:
        return render(request, 'users/user_profile.html', {'user': user, 'reviews': reviews})


@login_required
def my_user_profile(request):
    return redirect('anime_reviews:user_profile', user_pk=request.user.pk)


def login_and_signup(request):
    signUpForm = UserRegistrationForm()
    if request.method == 'POST':
        loginForm = UserLoginForm(request.POST)
        next = ''
        if 'url' in request.POST.keys():
            next = request.POST['url']
        if loginForm.is_valid():
            try:
                user = authenticate(username=request.POST['username'], password=request.POST['password'])
                login(request, user)
                if next != "":
                    return redirect(next)
                else:
                    return redirect(settings.LOGIN_REDIRECT_URL)
            except AttributeError:
                message = 'Please enter a correct username and password. Note that both fields may be case-sensitive.'
                return render(request, 'registration/login.html',
                              {'s_form': signUpForm, 'l_form': loginForm, 'message': message})
        else:
            message = 'Please enter a correct username and password. Note that both fields may be case-sensitive.'
            return render(request, 'registration/login.html', { 's_form' : signUpForm, 'l_form': loginForm,'message' : message } )

    else:
        loginForm = UserLoginForm()
        return render(request, 'registration/login.html', { 's_form' : signUpForm, 'l_form': loginForm} )



def register(request):
    signUpForm = UserRegistrationForm()
    loginForm = UserLoginForm()
    if request.method == 'POST':
        next = ''
        if 'url' in request.POST.keys():
            next = request.POST['url']
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)
            profile = UserProfile(user=user)
            profile.save()
            if next != "":
                return redirect(next)
            else:
                return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            message = 'Please check the data you entered'
            return render(request, 'registration/login.html', {'s_form': signUpForm, 'l_form': loginForm, 'message':message})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        try:
            profile = UserProfile.objects.get(user=user.pk)
            form = UserProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('anime_reviews:user_profile')
            else:
                message = "Please check data entered."
                return render(request, reverse('anime_reviews:edit_profile'), {'message': message, 'form': form})
        except UserProfile.DoesNotExist:
            form = UserProfileForm(request.POST)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = user
                profile.save()
                return redirect('anime_reviews:my_user_profile')
    else:
        form = UserProfileForm()
        return render(request, 'users/edit_profile.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


def meeting_place(request):
    key = os.environ.get('GOOGLE_MAP_KEY')
    return render(request, 'anime_reviews/directions/meeting.html', {'key':key})


def announcements(request, message=None):
    announcements = Announcement.objects.all().order_by('posted_date').reverse()
    if message:
        return render(request, 'anime_reviews/announcements/club_page.html', {'announcements': announcements, 'message':message})
    else:
        return render(request, 'anime_reviews/announcements/club_page.html', {'announcements': announcements})


def announcement_detail(request, id):
    try:
        announcement = Announcement.objects.get(id=id)
        return render(request, 'anime_reviews/announcements/announcement_detail.html', {'a':announcement})
    except Announcement.DoesNotExist:
        message = "Announcement was not found"
        return redirect('anime_reviews:announcements', message=message)
