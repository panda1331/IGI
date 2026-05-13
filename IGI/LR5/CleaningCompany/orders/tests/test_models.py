from django.test import TestCase
from orders.models import Order, OrderItem
from users.models import User
from services.models import Service, Category


class OrderModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username='client_test',
            password='test123',
            user_type='client',
            phone_number='+375 (29) 111-22-33'
        )
        Order.objects.create(
            client=User.objects.get(id=1),
            address='Test Address',
            work_date='2026-05-15',
            status='issued'
        )
        Category.objects.create(name='Test Category')
        Service.objects.create(
            name='Test Service',
            price=50.00,
            category=Category.objects.get(id=1)
        )

    def test_code_is_uuid(self):
        order = Order.objects.get(id=1)
        self.assertIsNotNone(order.code)

    def test_status_default(self):
        order = Order.objects.get(id=1)
        field_value = order.status
        self.assertEqual(field_value, 'issued')

    def test_status_max_length(self):
        order = Order.objects.get(id=1)
        field_max_length = order._meta.get_field('status').max_length
        self.assertEqual(field_max_length, 20)

    def test_address_max_length(self):
        order = Order.objects.get(id=1)
        field_max_length = order._meta.get_field('address').max_length
        self.assertEqual(field_max_length, 120)

    def test_order_str(self):
        order = Order.objects.get(id=1)
        self.assertIn('Order:', str(order))

    def test_total_price(self):
        OrderItem.objects.create(
            order=Order.objects.get(id=1),
            service=Service.objects.create(
                name='Second Service',
                price=25.00,
                category=Category.objects.get(id=1)
            ),
            quantity=1,
            price=25.00
        )
        order = Order.objects.get(id=1)
        self.assertEqual(order.total_price, 25.00)

class OrderItemModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username='client_test2',
            password='test123',
            user_type='client',
            phone_number='+375 (29) 222-33-44'
        )
        Category.objects.create(name='Test Category')
        Service.objects.create(
            name='Test Service',
            price=50.00,
            category=Category.objects.get(id=1)
        )
        Order.objects.create(
            client=User.objects.get(id=1),
            address='Address',
            work_date='2026-05-15'
        )
        OrderItem.objects.create(
            order=Order.objects.get(id=1),
            service=Service.objects.get(id=1),
            quantity=2,
            price=50.00
        )

    def test_quantity_value(self):
        order_item = OrderItem.objects.get(id=1)
        field_value = order_item.quantity
        self.assertEqual(field_value, 2)

    def test_price_value(self):
        order_item = OrderItem.objects.get(id=1)
        field_value = order_item.price
        self.assertEqual(field_value, 50.00)

    def test_order_item_str(self):
        order_item = OrderItem.objects.get(id=1)
        field_value = str(order_item)
        self.assertIn('Test Service', field_value)