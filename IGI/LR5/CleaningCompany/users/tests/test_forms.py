import datetime
from django.test import TestCase
from users.forms import UserRegisterForm, UserUpdateForm
from users.models import User

class UserRegisterFormTest(TestCase):

    def test_form_fields_exist(self):
        form = UserRegisterForm()
        self.assertIn('username', form.fields)
        self.assertIn('email', form.fields)
        self.assertIn('phone_number', form.fields)
        self.assertIn('date_of_birth', form.fields)
        self.assertIn('password', form.fields)

    def test_form_valid(self):
        form_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'middle_name': 'Testovich',
            'phone_number': '+375 (29) 111-22-33',
            'date_of_birth': '1995-05-10',
            'client_type': 'individual',
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_phone(self):
        form_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'phone_number': '12345',
            'date_of_birth': '1995-05-10',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_individual_with_company(self):
        form_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'phone_number': '+375 (29) 111-22-33',
            'date_of_birth': '1995-05-10',
            'client_type': 'individual',
            'company_name': 'Some Company',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_legal_without_company(self):
        form_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'phone_number': '+375 (29) 111-22-33',
            'date_of_birth': '1995-05-10',
            'client_type': 'legal',
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_legal_with_company(self):
        form_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'middle_name': 'Testovich',
            'phone_number': '+375 (29) 111-22-33',
            'date_of_birth': '1995-05-10',
            'client_type': 'individual',
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_save(self):
        form_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'middle_name': 'Testovich',
            'phone_number': '+375 (29) 111-22-33',
            'date_of_birth': '1995-05-10',
            'client_type': 'individual',
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.user_type, 'client')
        self.assertTrue(user.check_password('testpass123'))


class UserUpdateFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='test123',
            phone_number='+375 (29) 111-22-33'
        )

    def test_form_fields_exist(self):
        form = UserUpdateForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('email', form.fields)

    def test_form_update(self):
        form_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com',
        }
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        form.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.email, 'updated@example.com')