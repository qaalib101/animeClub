from django.test import TestCase, Client
from django.forms import ValidationError
from django.urls import reverse
from anime_reviews.models import Review
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

class TestUserView(TestCase):
    fixtures=['test_users', 'test_reviews']
    def test_user_with_reviews(self):
        user = User.objects.get(pk='1')
        self.client.force_login(user)
        response = self.client.get(reverse('anime_reviews:user_profile', kwargs={'user_pk': 1}))
        review = response.context['reviews'][0]
        expected = Review.objects.get(anime_id=20507)
        self.assertTemplateUsed(response, 'users/user_profile.html')
        self.assertEqual(review, expected)

    def test_user_without_reviews(self):
        user = User.objects.get(pk='3')
        self.client.force_login(user)
        response = self.client.get(reverse('anime_reviews:user_profile', kwargs={'user_pk': 3}))
        self.assertTemplateUsed(response, 'users/user_profile.html')
        self.assertContains(response, 'You have no reviews yet!')
