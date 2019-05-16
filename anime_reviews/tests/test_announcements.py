from django.test import TestCase, Client
from django.forms import ValidationError
from django.urls import reverse
from django.contrib import auth
from anime_reviews.models import Review, Announcement
from anime_reviews.forms import UserRegistrationForm, ReviewForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import re, datetime
from datetime import timezone

class TestAnnouncementView(TestCase):
    fixtures = ['test_announcements']

    def test_announcement_order(self):
        response = self.client.get(reverse('anime_reviews:announcements'))
        self.assertEqual(response.status_code, 200)
        a = response.context['announcements'][0]
        self.assertContains(response, "A new member has joined the club")
        expected = Announcement.objects.get(pk=2)
        self.assertEqual(a, expected)

    def test_fake_announcement_detail(self):
        response = self.client.get(reverse('anime_reviews:announcement_detail', kwargs={'id':3}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Announcement was not found')
        self.assertTemplateUsed(response, 'anime_reviews/announcements/club_page.html')

    def test_good_annuncement(self):
        response = self.client.get(reverse('anime_reviews:announcement_detail', kwargs={'id': 2}), follow=True)
        self.assertEqual(response.status_code, 200)
        a = Announcement.objects.get(id=2)
        expected = response.context['a']
        self.assertEqual(a, expected)
        self.assertTemplateUsed(response, 'anime_reviews/announcements/announcement_detail.html')


class TestEditAnnouncement(TestCase):
    fixtures = ['test_announcements', 'test_users']

    def test_edit_announcement(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        response = self.client.get(f'/club/announcements/edit/{1}', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'anime_reviews/announcements/edit_announcement.html')

