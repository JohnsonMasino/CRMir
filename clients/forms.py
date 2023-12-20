from django import forms

from classes import CustomBaseForm
from clients.models import Client


class ClientForm(CustomBaseForm, forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
