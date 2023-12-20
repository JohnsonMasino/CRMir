from django import forms

from classes import CustomBaseForm
from .models import Product


class ProductForm(CustomBaseForm, forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'product_description', 'unit_cost']
