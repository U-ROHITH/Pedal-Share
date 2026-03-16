from django import forms
from apps.complaints.models import Complaint


class ComplaintForm(forms.ModelForm):
    """Form for raising complaints"""
    class Meta:
        model = Complaint
        fields = ['category', 'subject', 'description']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief subject'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe your issue in detail'}),
        }
