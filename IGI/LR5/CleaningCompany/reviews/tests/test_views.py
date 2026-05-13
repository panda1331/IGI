from django.test import TestCase
from django.urls import reverse
from reviews.models import Review
from users.models import User

class ReviewViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='test123',
            user_type='client',
            phone_number='+375 (29) 111-11-11'
        )
        Review.objects.create(user=cls.user, score=5, text='Test review')

    def test_reviews_url_exists(self):
        resp = self.client.get('/reviews/')
        self.assertEqual(resp.status_code, 200)

    def test_reviews_accessible_by_name(self):
        resp = self.client.get(reverse('reviews'))
        self.assertEqual(resp.status_code, 200)

    def test_reviews_uses_correct_template(self):
        resp = self.client.get(reverse('reviews'))
        self.assertTemplateUsed(resp, 'reviews/reviews.html')

    def test_create_review_url_exists(self):
        self.client.login(username='testuser', password='test123')
        resp = self.client.get('/reviews/create/')
        self.assertEqual(resp.status_code, 200)

    def test_create_review_accessible_by_name(self):
        self.client.login(username='testuser', password='test123')
        resp = self.client.get(reverse('create_review'))
        self.assertEqual(resp.status_code, 200)

    def test_create_review_uses_correct_template(self):
        self.client.login(username='testuser', password='test123')
        resp = self.client.get(reverse('create_review'))
        self.assertTemplateUsed(resp, 'reviews/create_review.html')

    def test_create_review_post_valid(self):
        self.client.login(username='testuser', password='test123')
        resp = self.client.post(reverse('create_review'), {
            'score': 4,
            'text': 'Nice!'
        })
        self.assertRedirects(resp, reverse('reviews'))
        self.assertEqual(Review.objects.count(), 2)

    def test_create_review_post_invalid(self):
        self.client.login(username='testuser', password='test123')
        resp = self.client.post(reverse('create_review'), {
            'score': 10,
            'text': ''
        })
        self.assertEqual(resp.status_code, 200)

    def test_create_review_requires_login(self):
        resp = self.client.get(reverse('create_review'))
        self.assertEqual(resp.status_code, 302)