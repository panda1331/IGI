import datetime

from django.test import TestCase
from django.urls import reverse
from users.models import User
from orders.models import Order, OrderItem
from payments.models import Payment
from services.models import Category, Service


class StatsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser(username='admin', password='admin')
        category = Category.objects.create(name='Test')
        service = Service.objects.create(name='Test', price=10.00, category=category)
        client_user = User.objects.create_user(
            username='client_test',
            password='test123',
            user_type='client',
            phone_number='+375 (29) 111-11-11',
            date_of_birth='1990-01-01'
        )
        order = Order.objects.create(
            client=client_user,
            address='Test',
            work_date=datetime.date.today(),
            status='issued'
        )
        OrderItem.objects.create(order=order, service=service, quantity=1, price=10.00)
        Payment.objects.create(order=order, amount=10.00, status='paid')

    def test_statistics_url_requires_admin(self):
        resp = self.client.get('/statistics/')
        self.assertNotEqual(resp.status_code, 200)

    def test_statistics_accessible_by_admin(self):
        self.client.login(username='admin', password='admin')
        resp = self.client.get(reverse('statistics'))
        self.assertEqual(resp.status_code, 200)

    def test_statistics_uses_correct_template(self):
        self.client.login(username='admin', password='admin')
        resp = self.client.get(reverse('statistics'))
        self.assertTemplateUsed(resp, 'stats/statistics.html')

    def test_show_planned_works_accessible(self):
        self.client.login(username='admin', password='admin')
        resp = self.client.get(reverse('show_planned_works'))
        self.assertEqual(resp.status_code, 200)

    def test_show_planned_works_template(self):
        self.client.login(username='admin', password='admin')
        resp = self.client.get(reverse('show_planned_works'))
        self.assertTemplateUsed(resp, 'stats/show_planned_works.html')

    def test_client_cost_accessible(self):
        self.client.login(username='admin', password='admin')
        resp = self.client.get(reverse('client_cost'))
        self.assertEqual(resp.status_code, 200)

    def test_client_cost_template(self):
        self.client.login(username='admin', password='admin')
        resp = self.client.get(reverse('client_cost'))
        self.assertTemplateUsed(resp, 'stats/client_cost.html')

    def test_employee_clients_accessible(self):
        self.client.login(username='admin', password='admin')
        resp = self.client.get(reverse('employee_clients'))
        self.assertEqual(resp.status_code, 200)

    def test_employee_clients_template(self):
        self.client.login(username='admin', password='admin')
        resp = self.client.get(reverse('employee_clients'))
        self.assertTemplateUsed(resp, 'stats/employee_clients.html')