from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^promo-codes/$', views.promo_codes, name='promo_codes'),
    re_path(r'^(?P<order_id>\d+)/$', views.payment_check, name='payment'),
    re_path(r'^(?P<order_id>\d+)/pay/$', views.pay_order, name='pay_order'),
]