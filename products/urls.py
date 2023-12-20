from django.urls import path
from . import views
app_name = 'products'

urlpatterns = [
    path('', views.products_list, name='products_list'),
    path('create/', views.create_product_view, name='create_product'),
    path('update/<int:pk>/', views.update_product_view, name='update_product'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
]
