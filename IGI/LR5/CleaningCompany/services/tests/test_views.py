from django.test import TestCase
from django.urls import reverse
from services.models import Category, Service
from users.models import User

class ServiceViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='Window Cleaning')
        cls.service = Service.objects.create(
            name='Window Washing',
            price=15.00,
            category=cls.category
        )
        cls.admin = User.objects.create_superuser(username='admin', password='admin')

    def test_catalog_url_exists(self):
        resp = self.client.get('/catalog/')
        self.assertEqual(resp.status_code, 200)

    def test_catalog_accessible_by_name(self):
        resp = self.client.get(reverse('catalog'))
        self.assertEqual(resp.status_code, 200)

    def test_catalog_uses_correct_template(self):
        resp = self.client.get(reverse('catalog'))
        self.assertTemplateUsed(resp, 'services/catalog.html')

    def test_service_detail_url_exists(self):
        resp = self.client.get(f'/catalog/service/{self.service.id}/')
        self.assertEqual(resp.status_code, 200)

    def test_service_detail_accessible_by_name(self):
        resp = self.client.get(reverse('service_detail', kwargs={'pk': self.service.id}))
        self.assertEqual(resp.status_code, 200)

    def test_service_detail_uses_correct_template(self):
        resp = self.client.get(reverse('service_detail', kwargs={'pk': self.service.id}))
        self.assertTemplateUsed(resp, 'services/service_detail.html')

    def test_service_detail_returns_404(self):
        resp = self.client.get(reverse('service_detail', kwargs={'pk': 999}))
        self.assertEqual(resp.status_code, 404)

    def test_create_service_requires_admin(self):
        resp = self.client.get(reverse('create_service'))
        self.assertNotEqual(resp.status_code, 200)

    def test_create_service_admin_get(self):
        self.client.login(username='admin', password='admin')
        resp = self.client.get(reverse('create_service'))
        self.assertEqual(resp.status_code, 200)

    def test_create_service_admin_post(self):
        self.client.login(username='admin', password='admin')
        resp = self.client.post(reverse('create_service'), {
            'name': 'New Service',
            'price': '25.00',
            'category': self.category.id,
            'description': 'New description'
        })
        self.assertRedirects(resp, reverse('catalog'))
        self.assertEqual(Service.objects.count(), 2)

    def test_edit_service_admin_get(self):
        self.client.login(username='admin', password='admin')
        resp = self.client.get(reverse('edit_service', kwargs={'pk': self.service.id}))
        self.assertEqual(resp.status_code, 200)

    def test_delete_service_admin_post(self):
        self.client.login(username='admin', password='admin')
        resp = self.client.post(reverse('delete_service', kwargs={'pk': self.service.id}))
        self.assertRedirects(resp, reverse('catalog'))
        self.assertEqual(Service.objects.count(), 0)

    def test_create_category_admin_post(self):
        self.client.login(username='admin', password='admin')
        resp = self.client.post(reverse('create_category'), {'name': 'New Category'})
        self.assertRedirects(resp, reverse('catalog'))
        self.assertEqual(Category.objects.count(), 2)

    def test_edit_category_admin_get(self):
        self.client.login(username='admin', password='admin')
        resp = self.client.get(reverse('edit_category', kwargs={'pk': self.category.id}))
        self.assertEqual(resp.status_code, 200)

    def test_delete_category_admin_post(self):
        cat = Category.objects.create(name='To Delete')
        self.client.login(username='admin', password='admin')
        resp = self.client.post(reverse('delete_category', kwargs={'pk': cat.id}))
        self.assertRedirects(resp, reverse('catalog'))
        self.assertEqual(Category.objects.count(), 1)