# banking/forms.py
from django import forms
from .models import HelpTicket

class HelpTicketForm(forms.Form): # Or forms.ModelForm if you prefer
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief summary of your issue'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Please describe the problem in detail'})
    )

    # If using forms.ModelForm, it's simpler:
    # class Meta:
    #     model = HelpTicket
    #     fields = ['subject', 'message']
    #     widgets = {
    #         'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief summary of your issue'}),
    #         'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Please describe the problem in detail'}),
    #     }
