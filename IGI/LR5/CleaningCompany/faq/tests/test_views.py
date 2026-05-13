from django.test import TestCase
from django.urls import reverse

from faq.models import FAQ


class FAQViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(5):
            FAQ.objects.create(question=f'Question{i}', answer=f'Answer{i}')

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/faq/')
        self.assertEqual(resp.status_code, 200)

    def test_view_accessible_by_name(self):
        resp = self.client.get(reverse('faq'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('faq'))
        self.assertTemplateUsed(resp, 'faq/faqs.html')

    def test_lists_all_faqs(self):
        resp = self.client.get(reverse('faq'))
        self.assertEqual(len(resp.context['faqs']), 5)