
from django import forms
from .models import Deal
from contacts.models import Contact


class DealForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        company_id = self.data.get('company')

        if company_id:
            self.fields['contact'].queryset = Contact.objects.filter(
                company_id=company_id
            )
        else:
            self.fields['contact'].queryset = Contact.objects.none()

    class Meta:
        model = Deal

        fields = [
            'title',
            'company',
            'contact',
            'assigned_to',
            'value',
            'stage',
            'expected_close_date',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter deal title',
            }),
            'company': forms.Select(attrs={
                'class': 'form-control',
            }),
            'contact': forms.Select(attrs={
                'class': 'form-control',
            }),
            'assigned_to': forms.Select(attrs={
                'class': 'form-control',
            }),
            'value': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter deal value',
                'step': '0.01',
                'min': '0',
            }),
            'stage': forms.Select(attrs={
                'class': 'form-control',
            }),
            'expected_close_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }

        labels = {
            'title': 'Deal Name',
            'company': 'Company',
            'contact': 'Contact Person',
            'assigned_to': 'Responsible Employee',
            'value': 'Deal Value',
            'stage': 'Deal Stage',
            'expected_close_date': 'Expected Closing Date',
        }
