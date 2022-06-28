from django import forms
from verification.models import Document
from django.core.validators import MinLengthValidator


class DocumentForm(forms.ModelForm):

    institute_name = forms.CharField(max_length=100, validators=[MinLengthValidator(3)])
    holder_name = forms.CharField(max_length=100, validators=[MinLengthValidator(3)])
    
    class Meta:
        model = Document
        fields = [
            'institute_name',
            'holder_name',
            'document'
        ]