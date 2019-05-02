from django.test import TestCase, Client
from django.forms import ValidationError
from django.urls import reverse
from django.contrib import auth
from anime_reviews.models import Review
from anime_reviews.forms import UserRegistrationForm, ReviewForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import re, datetime
from datetime import timezone

class TestAnimeSearch(TestCase):
    fixtures = ['test_users', 'test_reviews']
    def test_empty_view(self):
        alice = User.objects.get(pk='1')
        self.client.force_login(alice)
        response = self.client.get(reverse('anime_reviews:anime_search'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('anime_reviews/reviews/anime_search.html')
        self.assertContains(response, 'Search for an anime tv show')
        review = response.context['reviews'][0]
        self.assertEqual(review.anime_id, 269)

    def test_search(self):
        response = self.client.post(reverse('anime_reviews:anime_search'), {'anime_search': 'noragami'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Search for an anime tv show')


class TestAnimeReviews(TestCase):
    fixtures = ['test_reviews', 'test_users']
    def test_incorrect_anime_id(self):
        user = User.objects.first()
        self.client.force_login(user)
        response = self.client.get(reverse('anime_reviews:new_review', kwargs={'anime_id': 2}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'anime_reviews/reviews/anime_search.html')
        self.assertContains(response, '2 is not a correct id for an anime.')
        response2 = self.client.get(reverse('anime_reviews:anime_detail', kwargs={'anime_id': 2}))
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, 'anime_reviews/reviews/anime_search.html')
        self.assertContains(response2, '2 is not a correct id for an anime.')

    def test_reviews_for_specific_anime(self):
        response = self.client.get(reverse('anime_reviews:anime_detail', kwargs={'anime_id': 20507}))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'No reviews for this anime')
        review = response.context['reviews'][0]
        expected = Review.objects.get(pk=1)
        self.assertEqual(review, expected)

class TestReviewForm(TestCase):
    fixtures = ['test_users', 'test_reviews']
    def test_add_review(self):
        self.client.force_login(User.objects.first())
        response = self.client.get(reverse('anime_reviews:new_review', kwargs={'anime_id':20507}), follow=True)
        self.assertTemplateUsed(response, 'anime_reviews/reviews/new_review.html')
    def test_post_wrong_review(self):
        self.client.force_login(User.objects.first())
        response = self.client.post(reverse('anime_reviews:new_review', kwargs={'anime_id': 20507}), follow=True)
        self.assertTemplateUsed(response, 'anime_reviews/reviews/new_review.html')
        self.assertContains(response, 'Enter correct information')

    def test_post_correct_review(self):
        self.client.force_login(User.objects.first())
        response = self.client.post(reverse('anime_reviews:new_review', kwargs={'anime_id': 20507}),
                                   {'comments': 'Good episode', 'episode': 1, 'season': 2, 'positive_review': True},
                                    follow=True)
        self.assertTemplateUsed(response, 'anime_reviews/reviews/review_detail.html')
        user = User.objects.first()
        expected = response.context['review']
        self.assertEqual(user, expected.user)
        self.assertEqual(6, expected.pk)


class TestDeleteView(TestCase):
    fixtures = ['test_users', 'test_reviews']
    def test_delete_reviews(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        response = self.client.get(reverse('anime_reviews:delete_review', kwargs={'review_id': 1}), follow=True)
        self.assertTemplateUsed(response, 'anime_reviews/reviews/review_detail.html')
        with self.assertRaises(Review.DoesNotExist):
            Review.objects.get(id=1)

    def test_delete_other_users_review(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        response = self.client.get(reverse('anime_reviews:delete_review', kwargs={'review_id': 2}), follow=True)
        self.assertTemplateUsed(response, 'anime_reviews/reviews/review_detail.html')
        review = Review.objects.get(id=2)


class TestEditReview(TestCase):
    fixtures = ['test_users', 'test_reviews']
    def test_edit_review(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        response = self.client.post(reverse('anime_reviews:edit_review', kwargs={'review_id': 1}),
                                    {'comments': 'Good episode', 'episode': 1, 'season': 2, 'positive_review': True},
                                    follow=True)
        self.assertTemplateUsed(response, 'anime_reviews/reviews/review_detail.html')
        review = Review.objects.get(id=1)
        self.assertEqual('Good episode', review.comments)
