from django.shortcuts import render, redirect

from .models import Review
from .forms import UserRegistrationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def user_profile(request, user_pk):
    user = User.objects.get(user=user_pk)
    return render(request, 'users/user_profile.html', {'user':user})


@login_required
def my_user_profile(request):
    return redirect('anime_reviews:user_profile', user_pk=request.user.pk)


def register(request):

    if request.method == 'POST':

        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)
            return redirect('anime_reviews:homepage')

        else :
            message = 'Please check the data you entered'
            return render(request, 'registration/register.html', { 'form' : form , 'message' : message } )


    else:
        form = UserRegistrationForm()
        return render(request, 'registration/register.html', { 'form' : form } )
