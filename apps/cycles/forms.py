from django import forms
from apps.cycles.models import Cycle


class CycleForm(forms.ModelForm):
    """Form for creating/editing cycles"""
    class Meta:
        model = Cycle
        fields = ['title', 'description', 'cycle_type', 'color', 'price_per_hour', 
                  'location', 'available_from', 'available_until', 'image', 'registration_number']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cycle title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe your cycle'}),
            'cycle_type': forms.Select(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Color'}),
            'price_per_hour': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pick-up location'}),
            'available_from': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'available_until': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'registration_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Registration number (optional)'}),
        }


class CycleFilterForm(forms.Form):
    """Form for filtering available cycles"""
    cycle_type = forms.ChoiceField(
        choices=[('', 'All Types')] + Cycle.TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    min_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Min price', 'step': '0.01', 'min': '0'}),
    )
    max_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max price', 'step': '0.01', 'min': '0'}),
    )
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search location'}),
    )
