from django.test import TestCase

from faq.models import FAQ


class FAQModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        FAQ.objects.create(question='question', answer='answer')

    def test_question_label(self):
        faq = FAQ.objects.get(id=1)
        field_label = faq._meta.get_field('question').verbose_name
        self.assertEqual(field_label, 'question')

    def test_answer_label(self):
        faq = FAQ.objects.get(id=1)
        field_label = faq._meta.get_field('answer').verbose_name
        self.assertEqual(field_label, 'answer')

    def test_date_label(self):
        faq = FAQ.objects.get(id=1)
        field_label = faq._meta.get_field('date').verbose_name
        self.assertEqual(field_label, 'date')

    def test_question_max_length(self):
        faq = FAQ.objects.get(id=1)
        max_length = faq._meta.get_field('question').max_length
        self.assertEqual(max_length, 200)

    def test_str_method(self):
        faq = FAQ.objects.get(id=1)
        self.assertEqual(str(faq), 'question')