# projects/forms.py
from django import forms

from classes import CustomBaseForm
from .models import Project, ProjectTalent


class ProjectForm(CustomBaseForm, forms.ModelForm):
    talents = forms.ModelMultipleChoiceField(
        queryset=ProjectTalent.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Project
        fields = '__all__'


class ProjectTalentForm(CustomBaseForm, forms.ModelForm):
    class Meta:
        model = ProjectTalent
        fields = '__all__'
        widgets = {
            'talent': forms.Select(),
        }
