from django.test import TestCase, Client
from django.forms import ValidationError
from django.urls import reverse
from django.contrib import auth
from anime_reviews.forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import re, datetime
from datetime import timezone


class TestRegistrationForm(TestCase):
    def test_add_wrong_form(self):
        form = UserRegistrationForm(data={'username': 'qaalib','first_name': 'qaalib', 'last_name': 'farah',
                                          'password1': 'feRpj4w4pso3az', 'password2': 'feRpj4w4pso3az'})
        self.assertFalse(form.is_valid())

'''class TestLoginForm(TestCase):
    def test_add_wrong_form(self):
        form = UserLoginForm(data={'username': 'qaalib', ''})
        self.assertFalse(form.is_valid())
'''