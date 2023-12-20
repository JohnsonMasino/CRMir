# forms.py

from django import forms

from classes import CustomBaseForm
from .models import CompanySettings, Role


class RoleForm(CustomBaseForm, forms.ModelForm):
    class Meta:
        model = Role
        fields = '__all__'


class CompanySettingsForm(CustomBaseForm, forms.ModelForm):
    class Meta:
        model = CompanySettings
        fields = '__all__'
        widgets = {
            'invoice_theme': forms.Select(attrs={'class': 'form-control'}),
            'company_address': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Define choices for the invoice_theme field
        self.fields['invoice_theme'].widget.choices = [
            ('estate', 'Estate'),
            ('business', 'Business'),
            ('hosting', 'Hosting'),
        ]
