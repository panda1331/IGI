import datetime

from django.test import TestCase
from django.urls import reverse

from orders.models import Order
from users.models import User

from services.models import Category, Service
from users.models import Specialization, EmployeeProfile


class OrderViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client_user = User.objects.create_user(
            username='client_test',
            password='test123',
            user_type='client',
            phone_number='+375 (29) 111-11-11'
        )
        cls.order = Order.objects.create(
            client=cls.client_user,
            address='Test Address',
            work_date=datetime.date.today(),
            status='issued'
        )

    def test_orders_url_exists(self):
        self.client.login(username='client_test', password='test123')
        resp = self.client.get('/orders/my/')
        self.assertEqual(resp.status_code, 200)

    def test_orders_accessible_by_name(self):
        self.client.login(username='client_test', password='test123')
        resp = self.client.get(reverse('order_list'))
        self.assertEqual(resp.status_code, 200)

    def test_orders_uses_correct_template(self):
        self.client.login(username='client_test', password='test123')
        resp = self.client.get(reverse('order_list'))
        self.assertTemplateUsed(resp, 'orders/orders.html')

    def test_create_order_url_exists(self):
        self.client.login(username='client_test', password='test123')
        resp = self.client.get('/orders/create/')
        self.assertEqual(resp.status_code, 200)

    def test_create_order_accessible_by_name(self):
        self.client.login(username='client_test', password='test123')
        resp = self.client.get(reverse('create_order'))
        self.assertEqual(resp.status_code, 200)

    def test_create_order_uses_correct_template(self):
        self.client.login(username='client_test', password='test123')
        resp = self.client.get(reverse('create_order'))
        self.assertTemplateUsed(resp, 'orders/create_order.html')

    def test_edit_order_requires_superuser(self):
        self.client.login(username='client_test', password='test123')
        resp = self.client.get(reverse('edit_order', kwargs={'pk': self.order.id}))
        self.assertNotEqual(resp.status_code, 200)

    def test_delete_order_requires_superuser(self):
        self.client.login(username='client_test', password='test123')
        resp = self.client.get(reverse('delete_order', kwargs={'pk': self.order.id}))
        self.assertNotEqual(resp.status_code, 200)


    def test_create_order_redirect_if_not_client(self):
        emp = User.objects.create_user(
            username='emp', password='123',
            user_type='employee', phone_number='+375 (29) 222-22-22'
        )
        self.client.login(username='emp', password='123')
        resp = self.client.get(reverse('create_order'))
        self.assertRedirects(resp, reverse('profile'))

    def test_edit_order_admin_get(self):
        admin = User.objects.create_superuser(username='admin2', password='admin')
        self.client.login(username='admin2', password='admin')
        resp = self.client.get(reverse('edit_order', kwargs={'pk': self.order.id}))
        self.assertEqual(resp.status_code, 200)

    def test_delete_order_admin_post(self):
        admin = User.objects.create_superuser(username='admin3', password='admin')
        self.client.login(username='admin3', password='admin')
        resp = self.client.post(reverse('delete_order', kwargs={'pk': self.order.id}))
        self.assertRedirects(resp, reverse('order_list'))
        self.assertEqual(Order.objects.count(), 0)

    def test_create_order_post_invalid_empty(self):
        self.client.login(username='client_test', password='test123')
        resp = self.client.post(reverse('create_order'), {})
        self.assertEqual(resp.status_code, 200)