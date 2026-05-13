import datetime

from django.test import TestCase
from django.urls import reverse

from orders.models import Order
from payments.models import PromoCode, Payment
from users.models import User


class PaymentViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client_user = User.objects.create_user(
            username='client',
            password='test123',
            user_type='client',
            phone_number='+375 (29) 111-11-11'
        )
        cls.order = Order.objects.create(
            client=cls.client_user,
            address='Test',
            work_date=datetime.date.today(),
            status='issued'
        )
        cls.payment = Payment.objects.create(
            order=cls.order,
            amount=100.00,
            status='waiting'
        )
        PromoCode.objects.create(
            code='TEST10',
            discount_percentage=10,
            valid_from=datetime.date.today(),
            valid_until=datetime.date.today() + datetime.timedelta(days=10)
        )

    def test_promo_codes_url_exists(self):
        resp = self.client.get('/payments/promo-codes/')
        self.assertEqual(resp.status_code, 200)

    def test_promo_codes_accessible_by_name(self):
        resp = self.client.get(reverse('promo_codes'))
        self.assertEqual(resp.status_code, 200)

    def test_promo_codes_uses_correct_template(self):
        resp = self.client.get(reverse('promo_codes'))
        self.assertTemplateUsed(resp, 'payments/promo_codes.html')

    def test_payment_check_accessible(self):
        self.client.login(username='client', password='test123')
        resp = self.client.get(reverse('payment', kwargs={'order_id': self.order.id}))
        self.assertEqual(resp.status_code, 200)

    def test_payment_check_uses_correct_template(self):
        self.client.login(username='client', password='test123')
        resp = self.client.get(reverse('payment', kwargs={'order_id': self.order.id}))
        self.assertTemplateUsed(resp, 'payments/payment.html')

    def test_pay_order_post(self):
        self.client.login(username='client', password='test123')
        resp = self.client.post(reverse('pay_order', kwargs={'order_id': self.order.id}))
        self.assertRedirects(resp, reverse('profile'))
        self.payment.refresh_from_db()
        self.assertEqual(self.payment.status, 'paid')

    def test_pay_order_get_redirects(self):
        self.client.login(username='client', password='test123')
        resp = self.client.get(reverse('pay_order', kwargs={'order_id': self.order.id}))
        self.assertRedirects(resp, reverse('payment', kwargs={'order_id': self.order.id}))

    def test_payment_check_other_user_forbidden(self):
        other = User.objects.create_user(
            username='other',
            password='test123',
            user_type='client',
            phone_number='+375 (29) 222-22-22'
        )
        self.client.login(username='other', password='test123')
        resp = self.client.get(reverse('payment', kwargs={'order_id': self.order.id}))
        self.assertEqual(resp.status_code, 404)