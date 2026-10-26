
from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'company',
            'name',
            'job_title',
            'email',
            'phone',
        ]
