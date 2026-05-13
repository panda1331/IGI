from django.test import TestCase
from vacancies.models import Vacancy

class VacancyModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Vacancy.objects.create(
            name='Cleaner',
            description='Cleaning specialist needed',
            is_active=True
        )

    def test_name_label(self):
        vacancy = Vacancy.objects.get(id=1)
        field_label = vacancy._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        vacancy = Vacancy.objects.get(id=1)
        max_length = vacancy._meta.get_field('name').max_length
        self.assertEqual(max_length, 150)

    def test_is_active_default(self):
        vacancy = Vacancy.objects.get(id=1)
        self.assertTrue(vacancy.is_active)

    def test_created_at_auto(self):
        vacancy = Vacancy.objects.get(id=1)
        self.assertIsNotNone(vacancy.created_at)

    def test_vacancy_str(self):
        vacancy = Vacancy.objects.get(id=1)
        self.assertEqual(str(vacancy), 'Cleaner')