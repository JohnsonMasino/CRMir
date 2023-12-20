# forms.py

from django import forms

from classes import CustomBaseForm
from .models import Talent


class TalentForm(CustomBaseForm, forms.ModelForm):
    class Meta:
        model = Talent
        fields = '__all__'
