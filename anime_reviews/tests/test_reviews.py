from django.test import TestCase, Client
from django.forms import ValidationError
from django.urls import reverse
from django.contrib import auth
from anime_reviews.forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import re, datetime
from datetime import timezone

class TestAnimeSearch(TestCase):
    def test_empty_view(self):
        response = self.client.get(reverse('anime_reviews:anime_search'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('anime_reviews/reviews/anime_search.html')
        self.assertContains(response, 'Search for an anime tv show')

    def test_search(self):
        response = self.client.post(reverse('anime_reviews:anime_search'), {'anime_search': 'noragami'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Search for an anime tv show')
        self.assertContains(response, )
