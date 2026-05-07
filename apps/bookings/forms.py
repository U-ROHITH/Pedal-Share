from django import forms
from datetime import time
from apps.bookings.models import Booking


class BookingForm(forms.ModelForm):
    """Form for creating bookings"""
    class Meta:
        model = Booking
        fields = ['booking_date', 'pickup_time', 'dropoff_time', 'notes']
        widgets = {
            'booking_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'pickup_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'dropoff_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Special requests (optional)'}),
        }
