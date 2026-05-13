from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from main.models import AboutCompany
from news.models import Article


class MainViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        AboutCompany.objects.create(
            name='Room Shining',
            description='Cleaning company',
            history='2018 - founded',
            requisites='Company LLC',
            email='info@roomshining.by',
            phone='+375 (29) 111-22-33'
        )
        Article.objects.create(
            title='Test News',
            short_description='Short text',
            content='Full content',
            is_published=True
        )

    @patch('requests.get')
    def test_index_url_exists(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.side_effect = [
            {'quote': {'body': 'tests quote', 'author': 'tests author'}},
            {'fact': 'tests fact'}
        ]
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)

    @patch('requests.get')
    def test_index_accessible_by_name(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.side_effect = [
            {'quote': {'body': 'tests quote', 'author': 'tests author'}},
            {'fact': 'tests fact'}
        ]
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)

    @patch('requests.get')
    def test_index_uses_correct_template(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.side_effect = [
            {'quote': {'body': 'tests quote', 'author': 'tests author'}},
            {'fact': 'tests fact'}
        ]
        resp = self.client.get(reverse('index'))
        self.assertTemplateUsed(resp, 'main/index.html')

    def test_about_url_exists(self):
        resp = self.client.get(reverse('about'))
        self.assertEqual(resp.status_code, 200)

    def test_about_accessible_by_name(self):
        resp = self.client.get(reverse('about'))
        self.assertEqual(resp.status_code, 200)

    def test_about_uses_correct_template(self):
        resp = self.client.get(reverse('about'))
        self.assertTemplateUsed(resp, 'main/about.html')

    def test_privacy_policy_url_exists(self):
        resp = self.client.get(reverse('privacy-policy'))
        self.assertEqual(resp.status_code, 200)

    def test_privacy_policy_accessible_by_name(self):
        resp = self.client.get(reverse('privacy-policy'))
        self.assertEqual(resp.status_code, 200)

    def test_privacy_policy_uses_correct_template(self):
        resp = self.client.get(reverse('privacy-policy'))
        self.assertTemplateUsed(resp, 'main/privacy_policy.html')