from django import forms

from classes import CustomBaseForm
from quotations.models import Quotation


class QuotationForm(CustomBaseForm, forms.ModelForm):
    class Meta:
        model = Quotation
        fields = '__all__'

        widgets = {
            'quotation_date': forms.TextInput(attrs={'type': 'date'}),
        }
