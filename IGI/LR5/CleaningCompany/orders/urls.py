from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^my/$', views.orders, name='order_list'),
    re_path(r'^create/$', views.create_order, name='create_order'),
    re_path(r'^edit/(?P<pk>\d+)/$', views.edit_order, name='edit_order'),
    re_path(r'^delete/(?P<pk>\d+)/$', views.delete_order, name='delete_order'),
]