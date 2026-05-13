import datetime
from django.test import TestCase
from orders.forms import OrderCreateForm
from services.models import Category, Service
from users.models import User, EmployeeProfile, Specialization


class OrderFormTest(TestCase):
    def test_address_label(self):
        form = OrderCreateForm()
        self.assertEqual(form.fields['address'].label, 'Address')

    def test_address_max_length(self):
        form = OrderCreateForm()
        self.assertEqual(form.fields['address'].max_length, 120)

    def test_work_date_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form_data = {'address': 'Test', 'work_date': date}
        form = OrderCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_work_date_too_far(self):
        date = datetime.date.today() + datetime.timedelta(days=31)
        form_data = {'address': 'Test', 'work_date': date}
        form = OrderCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_work_date_today(self):
        category = Category.objects.create(name='Test')
        service = Service.objects.create(name='Test Service', price=10.00, category=category)
        spec = Specialization.objects.create(name='Test')
        emp = User.objects.create_user(
            username='emp', password='123',
            user_type='employee', phone_number='+375 (29) 111-11-11'
        )
        profile = EmployeeProfile.objects.create(user=emp)
        profile.specializations.add(spec)
        date = datetime.date.today()
        form_data = {
            'address': 'Test Address',
            'work_date': date,
            f'quantity_{service.id}': 1,
            'employee': emp.id
        }
        form = OrderCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_work_date_label(self):
        form = OrderCreateForm()
        self.assertEqual(form.fields['work_date'].label, 'Work Date')

    def test_promo_code_label(self):
        form = OrderCreateForm()
        self.assertEqual(form.fields['promo_code'].label, 'Promo Code')

    def test_employee_field_exists(self):
        form = OrderCreateForm()
        self.assertIn('employee', form.fields)

    def test_promo_code_optional(self):
        form = OrderCreateForm()
        self.assertFalse(form.fields['promo_code'].required)