from django.urls import re_path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    re_path(r'^contacts/$', views.contacts, name='contacts'),
    re_path(r'^login/$', LoginView.as_view(template_name='users/login.html'), name='login'),
    re_path(r'^logout/$', LogoutView.as_view(), name='logout'),
    re_path(r'^profile/$', views.profile, name='profile'),
    re_path(r'^register/$', views.register, name='register'),
    re_path(r'^profile/update/$', views.update_profile, name='profile_edit'),

    re_path(r'^manage/$', views.show_users, name='manage_users'),
    re_path(r'^manage/edit/(?P<pk>\d+)/$', views.edit_user, name='edit_user'),
    re_path(r'^manage/delete/(?P<pk>\d+)/$', views.delete_user, name='delete_user'),
    re_path(r'^manage/create_employee/$', views.create_employee, name='create_employee'),
]