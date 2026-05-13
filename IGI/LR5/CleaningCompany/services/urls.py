from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.catalog, name='catalog'),
    re_path(r'^service/(?P<pk>\d+)/$', views.service_detail, name='service_detail'),
    re_path(r'^create_service/$', views.create_service, name='create_service'),
    re_path(r'^edit_service/(?P<pk>\d+)/$', views.edit_service, name='edit_service'),
    re_path(r'^delete_service/(?P<pk>\d+)/$', views.delete_service, name='delete_service'),

    re_path(r'^create_category/$', views.create_category, name='create_category'),
    re_path(r'^edit_category/(?P<pk>\d+)/$', views.edit_category, name='edit_category'),
    re_path(r'^delete_category/(?P<pk>\d+)/$', views.delete_category, name='delete_category'),
]