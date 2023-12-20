from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('list/', views.payments_list, name='payment_list'),
    path('calculate_total_amount/<int:invoice_id>/', views.calculate_total_amount, name='calculate_total_amount'),
    path('reconcile/<int:payment_id>/', views.reconcile_payment, name='reconcile_payment'),
    path('resend/<int:payment_id>/', views.resend_payment, name='resend_payment'),
    path('reverse/<int:payment_id>/', views.reverse_payment, name='reverse_payment'),
    path('make_payment/', views.make_payment, name='make_payment'),
    path('make_payment/<int:invoice_id>/', views.make_payment, name='make_payment'),
]
