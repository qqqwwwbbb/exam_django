from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views

from .views import *

urlpatterns = [
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', DesLogoutView.as_view(), name='logout'),
    path('', index, name='index'),
    path('profile', profile, name='profile'),
    path('register', RegisterView.as_view(), name='register',),
    path('create_application', CreateApplication.as_view(), name='create_application'),
    path('view_applications', ViewApplicationsBorrower.as_view(), name='view_applications'),
    path('view_categories', ViewCategory.as_view(), name='view_categories'),
    path('view_categories/create_category', CreateCategory.as_view(), name='create_category'),
    re_path(r'^application/(?P<pk>\d+)/delete/$', DeleteApplication.as_view(), name='delete_application'),
    path(r'^application/(?P<pk>\w+)/(?P<st>\w+)/update/$', confirm_update, name='confirm_update'),
    re_path(r'^category/(?P<pk>\d+)/delete/$', DeleteCategory.as_view(), name='delete_category'),
]
