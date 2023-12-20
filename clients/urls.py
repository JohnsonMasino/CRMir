from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.clients_list, name='clients_list'),
    path('<int:client_id>/', views.view_client, name='view_client'),
    path('create/', views.create_client, name='create_client'),
    path('update/<int:client_id>/', views.update_client, name='update_client'),
    path('delete/<int:client_id>/', views.delete_client, name='delete_client'),
]
