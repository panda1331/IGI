from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.reviews, name='reviews'),
    re_path(r'^create/$', views.create_review, name='create_review'),
]