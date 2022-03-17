from .models import My_model
from django import forms


class Upload(forms.ModelForm):
    class Meta:
        model = My_model
        fields =['pdf']