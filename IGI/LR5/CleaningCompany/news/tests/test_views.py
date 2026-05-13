from django.test import TestCase
from django.urls import reverse
from news.models import Article

class ArticleViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Article.objects.create(
            title='Test News',
            short_description='Short text',
            content='Full content',
            is_published=True
        )

    def test_articles_url_exists(self):
        resp = self.client.get('/news/')
        self.assertEqual(resp.status_code, 200)

    def test_articles_accessible_by_name(self):
        resp = self.client.get(reverse('article_list'))
        self.assertEqual(resp.status_code, 200)

    def test_articles_uses_correct_template(self):
        resp = self.client.get(reverse('article_list'))
        self.assertTemplateUsed(resp, 'news/articles.html')

    def test_article_detail_url_exists(self):
        resp = self.client.get('/news/article/1/')
        self.assertEqual(resp.status_code, 200)

    def test_article_detail_accessible_by_name(self):
        resp = self.client.get(reverse('article_info', kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 200)

    def test_article_detail_uses_correct_template(self):
        resp = self.client.get(reverse('article_info', kwargs={'pk': 1}))
        self.assertTemplateUsed(resp, 'news/article_info.html')

    def test_article_detail_returns_404(self):
        resp = self.client.get(reverse('article_info', kwargs={'pk': 999}))
        self.assertEqual(resp.status_code, 404)