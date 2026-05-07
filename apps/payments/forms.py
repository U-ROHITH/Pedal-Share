from django import forms
from apps.payments.models import Transaction


class WalletTopupForm(forms.Form):
    """Form for wallet top-ups"""
    AMOUNT_CHOICES = [
        ('250', '₹250'),
        ('500', '₹500'),
        ('1000', '₹1,000'),
        ('2000', '₹2,000'),
        ('5000', '₹5,000'),
        ('custom', 'Custom Amount'),
    ]
    
    amount_preset = forms.ChoiceField(
        choices=AMOUNT_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        required=True
    )
    custom_amount = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter custom amount',
            'step': '0.01',
            'min': '10'
        })
    )
