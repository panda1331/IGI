import datetime

from django.test import TestCase

from orders.models import Order
from payments.models import Payment, PromoCode
from users.models import User


class PaymentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        client = User.objects.create_user(
            username='client',
            password='test123',
            user_type='client',
            phone_number='+375 (29) 111-11-11'
        )
        cls.order = Order.objects.create(
            client=client,
            address='Address',
            work_date=datetime.date.today(),
            status='issued'
        )
        Payment.objects.create(
            order=cls.order,
            amount=100.00,
            status='waiting',
            payment_method='card'
        )

    def test_amount_value(self):
        payment = Payment.objects.get(id=1)
        field_value = payment.amount
        self.assertEqual(field_value, 100.00)

    def test_status_default(self):
        payment = Payment.objects.get(id=1)
        field_value = payment.status
        self.assertEqual(field_value, 'waiting')

    def test_status_max_length(self):
        payment = Payment.objects.get(id=1)
        field_max_length = payment._meta.get_field('status').max_length
        self.assertEqual(field_max_length, 10)

    def test_payment_method_max_length(self):
        payment = Payment.objects.get(id=1)
        field_max_length = payment._meta.get_field('payment_method').max_length
        self.assertEqual(field_max_length, 10)

    def test_payment_method_default(self):
        payment = Payment.objects.get(id=1)
        self.assertEqual(payment.payment_method, 'card')

    def test_paid_at_null(self):
        payment = Payment.objects.get(id=1)
        self.assertIsNone(payment.paid_at)

    def test_payment_str(self):
        payment = Payment.objects.get(id=1)
        self.assertIn('Payment order:', str(payment))

class PromoCodeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        PromoCode.objects.create(
            code='TEST10',
            discount_percentage=10,
            valid_from=datetime.date.today(),
            valid_until=datetime.date.today() + datetime.timedelta(days=10)
        )

    def test_code_max_length(self):
        promo = PromoCode.objects.get(id=1)
        field_max_length = promo._meta.get_field('code').max_length
        self.assertEqual(field_max_length, 10)

    def test_code_unique(self):
        promo = PromoCode.objects.get(id=1)
        field_unique = promo._meta.get_field('code').unique
        self.assertTrue(field_unique)

    def test_discount_percentage_value(self):
        promo = PromoCode.objects.get(id=1)
        field_value = promo.discount_percentage
        self.assertEqual(field_value, 10)

    def test_is_active_true(self):
        promo = PromoCode.objects.get(id=1)
        self.assertTrue(promo.is_active)

    def test_is_active_false_expired(self):
        promo = PromoCode.objects.create(
            code='EXPIRED',
            discount_percentage=5,
            valid_from=datetime.date.today() - datetime.timedelta(days=20),
            valid_until=datetime.date.today() - datetime.timedelta(days=1)
        )
        self.assertFalse(promo.is_active)

    def test_promo_code_str(self):
        promo = PromoCode.objects.get(id=1)
        field_value = str(promo)
        self.assertIn('TEST10', field_value)