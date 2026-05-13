from django.test import TestCase
from main.models import AboutCompany


class AboutCompanyTest(TestCase):
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

    def test_name_label(self):
        obj = AboutCompany.objects.get(id=1)
        field_name = obj._meta.get_field('name').verbose_name
        self.assertEqual(field_name, 'name')

    def test_name_max_length(self):
        obj = AboutCompany.objects.get(id=1)
        max_length = obj._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_phone_max_length(self):
        obj = AboutCompany.objects.get(id=1)
        max_length = obj._meta.get_field('phone').max_length
        self.assertEqual(max_length, 20)

    def test_str_method(self):
        obj = AboutCompany.objects.get(id=1)
        self.assertEqual(str(obj), 'Room Shining')