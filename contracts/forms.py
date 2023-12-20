# contracts/forms.py
from django import forms

from classes import CustomBaseForm
from .models import Contract


class ContractForm(CustomBaseForm, forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['contract_reference', 'contract_expiration_date', 'contract_status']
