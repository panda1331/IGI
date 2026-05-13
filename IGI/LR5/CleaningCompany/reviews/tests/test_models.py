from django.test import TestCase

from reviews.models import Review
from users.models import User


class ReviewModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='test123',
            user_type='client',
            phone_number='+375 (29) 111-11-11'
        )
        Review.objects.create(
            user=cls.user,
            score=5,
            text='Great service!'
        )

    def test_score_value(self):
        review = Review.objects.get(id=1)
        field_value = review.score
        self.assertEqual(field_value, 5)

    def test_text_value(self):
        review = Review.objects.get(id=1)
        field_value = review.text
        self.assertEqual(field_value, 'Great service!')

    def test_created_at_auto(self):
        review = Review.objects.get(id=1)
        self.assertIsNotNone(review.created_at)

    def test_user_relation(self):
        review = Review.objects.get(id=1)
        self.assertEqual(review.user.username, 'testuser')

    def test_review_str(self):
        review = Review.objects.get(id=1)
        field_value = str(review)
        self.assertEqual(field_value, 'Great service!')