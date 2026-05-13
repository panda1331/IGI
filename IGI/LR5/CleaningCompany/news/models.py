from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=120)
    short_description = models.CharField(max_length=250)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='news_images', null=True, blank=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title
