# contracts/urls.py
from django.urls import path
from . import views

app_name = 'contracts'

urlpatterns = [
    path('', views.contracts_list, name='contracts_list'),
    path('<int:pk>/', views.view_contract, name='view_contract'),
    path('create/<int:invoice_id>/', views.create_contract, name='create_contract'),
    path('update/<int:contract_id>/', views.update_contract, name='update_contract'),
    path('delete/<int:contract_id>/', views.delete_contract, name='delete_contract'),

]
