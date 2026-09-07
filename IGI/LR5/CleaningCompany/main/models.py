import re

from django.db import models

class AboutCompany(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='about/', blank=True)
    video = models.FileField(upload_to='videos/about', blank=True, null=True)
    description = models.TextField()
    history = models.TextField()

    requisites = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Partner(models.Model):
    name = models.CharField(max_length=100)
    logo = models.FileField(upload_to='partners/', blank=True)
    website_url = models.URLField()

    def __str__(self):
        return self.name
