# urls.py

from django.urls import path
from . import views

app_name = 'talents'

urlpatterns = [
    path('', views.talent_list, name='talent_list'),
    path('talents/create/', views.talent_create, name='talent_create'),
    path('talents/<int:talent_id>/update/', views.talent_update, name='talent_update'),
    path('talents/<int:talent_id>/delete/', views.talent_delete, name='talent_delete'),
]
