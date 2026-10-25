from django import forms
from .models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'name',
            'industry',
            'website',
            'phone',
            'email',
            'address',
            'city',
            
        ]