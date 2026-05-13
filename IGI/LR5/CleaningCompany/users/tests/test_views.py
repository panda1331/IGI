from django.test import TestCase
from django.urls import reverse
from users.models import User, EmployeeProfile, Specialization
from datetime import date

class UserViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client_user = User.objects.create_user(
            username='client',
            password='test123',
            user_type='client',
            phone_number='+375 (29) 111-22-33'
        )
        cls.employee = User.objects.create_user(
            username='employee',
            password='test123',
            first_name='Test',
            last_name='Employee',
            user_type='employee',
            phone_number='+375 (29) 444-44-44'
        )
        cls.spec = Specialization.objects.create(name='Cleaning')
        cls.profile = EmployeeProfile.objects.create(user=cls.employee)
        cls.profile.specializations.add(cls.spec)
        cls.admin = User.objects.create_superuser(username='admin', password='admin')

    def test_contacts_url_exists(self):
        resp = self.client.get('/accounts/contacts/')
        self.assertEqual(resp.status_code, 200)

    def test_contacts_accessible_by_name(self):
        resp = self.client.get(reverse('contacts'))
        self.assertEqual(resp.status_code, 200)

    def test_register_url_exists(self):
        resp = self.client.get('/accounts/register/')
        self.assertEqual(resp.status_code, 200)

    def test_register_accessible_by_name(self):
        resp = self.client.get(reverse('register'))
        self.assertEqual(resp.status_code, 200)

    def test_register_uses_correct_template(self):
        resp = self.client.get(reverse('register'))
        self.assertTemplateUsed(resp, 'users/register.html')

    def test_profile_requires_login(self):
        resp = self.client.get(reverse('profile'))
        self.assertEqual(resp.status_code, 302)

    def test_profile_accessible_when_logged_in(self):
        self.client.login(username='client', password='test123')
        resp = self.client.get(reverse('profile'))
        self.assertEqual(resp.status_code, 200)

    def test_profile_edit_accessible(self):
        self.client.login(username='client', password='test123')
        resp = self.client.get(reverse('profile_edit'))
        self.assertEqual(resp.status_code, 200)

    def test_manage_users_requires_admin(self):
        self.client.login(username='client', password='test123')
        resp = self.client.get(reverse('manage_users'))
        self.assertNotEqual(resp.status_code, 200)

    def test_manage_users_admin_accessible(self):
        self.client.login(username='admin', password='admin')
        resp = self.client.get(reverse('manage_users'))
        self.assertEqual(resp.status_code, 200)

    def test_edit_user_admin_accessible(self):
        self.client.login(username='admin', password='admin')
        resp = self.client.get(reverse('edit_user', kwargs={'pk': self.client_user.id}))
        self.assertEqual(resp.status_code, 200)

    def test_delete_user_admin_post(self):
        self.client.login(username='admin', password='admin')
        resp = self.client.post(reverse('delete_user', kwargs={'pk': self.client_user.id}))
        self.assertRedirects(resp, reverse('manage_users'))

    def test_create_employee_admin_get(self):
        self.client.login(username='admin', password='admin')
        resp = self.client.get(reverse('create_employee'))
        self.assertEqual(resp.status_code, 200)