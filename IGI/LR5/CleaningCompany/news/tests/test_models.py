from django.test import TestCase

from news.models import Article


class ArticleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Article.objects.create(
            title='Test News',
            short_description='Short text',
            content='Full content',
            is_published=True
        )

    def test_title_label(self):
        article = Article.objects.get(id=1)
        field_label = article._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_title_max_length(self):
        article = Article.objects.get(id=1)
        max_length = article._meta.get_field('title').max_length
        self.assertEqual(max_length, 120)

    def test_short_description_max_length(self):
        article = Article.objects.get(id=1)
        max_length = article._meta.get_field('short_description').max_length
        self.assertEqual(max_length, 250)

    def test_is_published_default(self):
        article = Article.objects.get(id=1)
        self.assertTrue(article.is_published)

    def test_str_method(self):
        article = Article.objects.get(id=1)
        self.assertEqual(str(article), 'Test News')