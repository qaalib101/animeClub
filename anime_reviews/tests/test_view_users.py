from django.test import TestCase, Client
from django.forms import ValidationError
from django.urls import reverse
from django.contrib import auth
from anime_reviews.forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import re, datetime
from datetime import timezone

class TestUserRegistration(TestCase):

    def test_add_correct_registration(self):
        response = self.client.post(reverse('anime_reviews:register'), {'username': 'qaalib', 'email': 'qaalib1598@gmail.com', 'first_name': 'qaalib', 'last_name': 'farah',
                                          'password1': 'feRpj4w4pso3az', 'password2': 'feRpj4w4pso3az'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'anime_reviews/home.html')

    def test_add_wrong_registration(self):
        response = self.client.post(reverse('anime_reviews:register'),
                                    {'username': 'qaalib', 'first_name': 'qaalib',
                                     'last_name': 'farah',
                                     'password1': 'feRpj4w4pso3az', 'password2': 'feRpj4w4pso3az'}, follow=True)
        self.assertContains(response, 'Please check the data you entered')


    def test_add_existing_email(self):
        response = self.client.post(reverse('anime_reviews:register'),
                                    {'username': 'qaalib', 'email': 'qaalib1598@gmail.com', 'first_name': 'qaalib',
                                     'last_name': 'farah',
                                     'password1': 'feRpj4w4pso3az', 'password2': 'feRpj4w4pso3az'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'anime_reviews/home.html')
        response2 = self.client.post(reverse('anime_reviews:register'),
                                    {'username': 'qaalib', 'first_name': 'qaalib',
                                     'last_name': 'farah',
                                     'password1': 'feRpj4w4pso3az', 'password2': 'feRpj4w4pso3az'}, follow=True)
        self.assertContains(response2, 'Please check the data you entered')
        self.assertEqual(response.status_code, 200)


class TestUserLogin(TestCase):
    def test_wrong_login(self):
        response = self.client.post(reverse('anime_reviews:login_and_signup'), {'username':'qaalib101', 'password': 'wrong_password'}, follow=True)
        self.assertContains(response, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')
        self.assertTemplateUsed(response, 'registration/login.html')
