from classes import CustomBaseForm
from .models import PaymentMethod

from django import forms
from .models import Payment, Invoice


class PaymentForm(CustomBaseForm, forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['invoice'].choices = [(invoice.id, str(invoice)) for invoice in Invoice.objects.all()]


class PaymentMethodForm(CustomBaseForm, forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = '__all__'
