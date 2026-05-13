from django.test import TestCase
from django.urls import reverse
from vacancies.models import Vacancy

class VacancyViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Vacancy.objects.create(
            name='Cleaner',
            description='Cleaning specialist needed'
        )

    def test_vacancies_url_exists(self):
        resp = self.client.get('/vacancies/')
        self.assertEqual(resp.status_code, 200)

    def test_vacancies_accessible_by_name(self):
        resp = self.client.get(reverse('vacancies'))
        self.assertEqual(resp.status_code, 200)

    def test_vacancies_uses_correct_template(self):
        resp = self.client.get(reverse('vacancies'))
        self.assertTemplateUsed(resp, 'vacancies/vacancies.html')

    def test_vacancies_context(self):
        resp = self.client.get(reverse('vacancies'))
        self.assertEqual(len(resp.context['vacancies']), 1)
        self.assertEqual(resp.context['vacancies'][0].name, 'Cleaner')