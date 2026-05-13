from django.test import TestCase
from services.models import Category, Service

class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Window Cleaning')

    def test_name_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        category = Category.objects.get(id=1)
        field_max_length = category._meta.get_field('name').max_length
        self.assertEqual(field_max_length, 100)

    def test_category_str(self):
        category = Category.objects.get(id=1)
        field_value = str(category)
        self.assertEqual(field_value, 'Window Cleaning')


class ServiceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='Window Cleaning')
        Service.objects.create(
            name='Window Washing',
            description='Wash windows',
            price=15.00,
            category=cls.category
        )

    def test_name_label(self):
        service = Service.objects.get(id=1)
        field_label = service._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        service = Service.objects.get(id=1)
        field_max_length = service._meta.get_field('name').max_length
        self.assertEqual(field_max_length, 100)

    def test_price_value(self):
        service = Service.objects.get(id=1)
        field_value = service.price
        self.assertEqual(field_value, 15.00)

    def test_category_relation(self):
        service = Service.objects.get(id=1)
        field_value = service.category.name
        self.assertEqual(field_value, 'Window Cleaning')

    def test_service_str(self):
        service = Service.objects.get(id=1)
        field_value = str(service)
        self.assertEqual(field_value, 'Window Washing')