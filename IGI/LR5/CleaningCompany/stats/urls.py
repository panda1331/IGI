from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.get_statistics, name='statistics'),
    re_path(r'^show_planned_works/$', views.show_planned_works, name='show_planned_works'),
    re_path(r'^client_cost/$', views.client_cost, name='client_cost'),
    re_path(r'^employee_clients/$', views.employee_clients, name='employee_clients'),
]