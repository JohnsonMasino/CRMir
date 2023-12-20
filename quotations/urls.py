from django.urls import path
from . import views

app_name = 'quotations'

urlpatterns = [
    path('', views.quotations_list, name='quotations_list'),
    path('create/', views.create_quotation, name='create_quotation'),
    path('<int:quotation_id>/', views.view_quotation, name='view_quotation'),
    path('<int:quotation_id>/delete/', views.delete_quotation, name='delete_quotation'),
]
