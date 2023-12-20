# urls.py

from django.urls import path, include
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('load_chart_data/', views.load_chart_data, name='load_chart_data'),
]
