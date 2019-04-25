from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import Http404

from .models import Review, UserProfile
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def user_profile(request, user_pk):
    user = User.objects.get(pk=user_pk)
    reviews = Review.objects.all().filter(user=user_pk).order_by('posted_date', 'likes')
    try:
        profile = get_object_or_404(UserProfile, user=user.pk)
        return render(request, 'users/user_profile.html', {'user': user, 'reviews': reviews, 'profile': profile})
    except Http404:
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
            profile = get_object_or_404(UserProfile, user=user.pk)
            form = UserProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('anime_reviews:user_profile')
            else:
                message = "Please check data entered."
                return render(request, reverse('anime_reviews:edit_profile'), {'message': message, 'form': form})
        except Http404:
            form = UserProfileForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('anime_reviews:user_profile')
    else:
        form = UserProfileForm()
        return render(request, 'users/edit_profile.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)
