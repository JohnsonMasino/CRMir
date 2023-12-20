from django.urls import path
from . import views

app_name = 'invoices'

urlpatterns = [
    path('', views.invoices_list, name='invoices_list'),  # Make sure the name is 'invoices_list'
    # URL pattern for creating a new invoice from a quotation
    path('create_invoice/', views.create_invoice_view, name='create_invoice'),
    path('create_invoice/<int:quotation_id>/', views.create_invoice_view, name='create_invoice'),
    path('view_invoice/<int:invoice_id>/', views.view_invoice, name='view_invoice'),
    path('delete/<int:invoice_id>/', views.delete_invoice, name='delete_invoice'),
    path('send_invoice_email/<int:invoice_id>/', views.view_invoice_pdf, name='send_invoice_email'),



]
