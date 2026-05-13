from django.test import TestCase

from reviews.forms import ReviewForm
from users.models import User


class ReviewFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='test123',
            user_type='client',
            phone_number='+375 (29) 111-11-11'
        )

    def test_form_fields_exist(self):
        form = ReviewForm()
        self.assertIn('score', form.fields)
        self.assertIn('text', form.fields)

    def test_form_valid(self):
        form_data = {'score': 5, 'text': 'Great!'}
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_score_low(self):
        form_data = {'score': 0, 'text': 'Bad'}
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_invalid_score_high(self):
        form_data = {'score': 6, 'text': 'Too high'}
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_invalid_empty_text(self):
        form_data = {'score': 3, 'text': ''}
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_save(self):
        form_data = {'score': 4, 'text': 'Nice'}
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())
        review = form.save(commit=False)
        review.user = self.user
        review.save()
        self.assertEqual(review.score, 4)
        self.assertEqual(review.text, 'Nice')