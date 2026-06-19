from django import forms
from .models import BlueprintSimpleModel


class BlueprintSimpleModelForm(forms.ModelForm):
    class Meta:
        model = BlueprintSimpleModel
        fields = ['name', 'description', 'parent']