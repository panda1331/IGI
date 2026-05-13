from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.articles, name='article_list'),
    re_path(r'^article/(?P<pk>\d+)/$', views.article_detail, name='article_info'),
]