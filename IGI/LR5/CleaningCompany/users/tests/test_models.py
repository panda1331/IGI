from django.test import TestCase
from users.models import User, Specialization, EmployeeProfile
from django.core.exceptions import ValidationError
from datetime import date

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='test123',
            first_name='Test',
            last_name='User',
            middle_name='Testovich',
            email='test@example.com',
            phone_number='+375 (29) 111-22-33',
            date_of_birth='1995-05-10',
            user_type='client',
            client_type='individual'
        )

    def test_user_creation(self):
        user = User.objects.get(id=1)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.middle_name, 'Testovich')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.phone_number, '+375 (29) 111-22-33')
        self.assertEqual(user.user_type, 'client')
        self.assertEqual(user.client_type, 'individual')

    def test_get_full_name(self):
        user = User.objects.get(id=1)
        self.assertEqual(user.get_full_name(), 'Test User')

    def test_user_type_default(self):
        user = User.objects.create_user(username='user2', password='123', phone_number='+375 (29) 222-22-33')
        self.assertEqual(user.user_type, 'client')

    def test_client_type_default(self):
        user = User.objects.create_user(username='user3', password='123', phone_number='+375 (29) 333-33-33')
        self.assertEqual(user.client_type, 'individual')

    def test_validate_age(self):
        user = User(username='young', phone_number='+375 (29) 444-44-44', date_of_birth='2020-01-01')
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_phone_regex_validator(self):
        user = User(username='badphone', phone_number='12345')
        with self.assertRaises(ValidationError):
            user.full_clean()


class SpecializationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Specialization.objects.create(name='Window Cleaning')

    def test_name_value(self):
        spec = Specialization.objects.get(id=1)
        self.assertEqual(spec.name, 'Window Cleaning')

    def test_name_max_length(self):
        spec = Specialization.objects.get(id=1)
        max_length = spec._meta.get_field('name').max_length
        self.assertEqual(max_length, 150)

    def test_specialization_str(self):
        spec = Specialization.objects.get(id=1)
        self.assertEqual(str(spec), 'Window Cleaning')


class EmployeeProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='employee',
            password='test123',
            first_name='Test',
            last_name='Employee',
            user_type='employee',
            phone_number='+375 (29) 555-55-55'
        )
        cls.spec = Specialization.objects.create(name='Cleaning')
        cls.profile = EmployeeProfile.objects.create(
            user=cls.user,
            hire_date=date.today(),
            description='Experienced cleaner'
        )
        cls.profile.specializations.add(cls.spec)

    def test_user_relation(self):
        profile = EmployeeProfile.objects.get(id=1)
        self.assertEqual(profile.user.username, 'employee')

    def test_specializations(self):
        profile = EmployeeProfile.objects.get(id=1)
        self.assertEqual(profile.specializations.count(), 1)
        self.assertEqual(profile.specializations.first().name, 'Cleaning')

    def test_hire_date_value(self):
        profile = EmployeeProfile.objects.get(id=1)
        self.assertEqual(profile.hire_date, date.today())

    def test_description_value(self):
        profile = EmployeeProfile.objects.get(id=1)
        self.assertEqual(profile.description, 'Experienced cleaner')

    def test_display_specializations(self):
        profile = EmployeeProfile.objects.get(id=1)
        self.assertEqual(profile.display_specializations(), 'Cleaning')

    def test_employee_profile_str(self):
        profile = EmployeeProfile.objects.get(id=1)
        self.assertIn('Employee', str(profile))