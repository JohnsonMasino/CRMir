# urls.py

from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
    path('', views.settings_view, name='settings'),
    path('profile', views.profile_page, name='profile_page'),
]
