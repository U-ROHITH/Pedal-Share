from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import datetime
from apps.core.models import BaseModel
from apps.cycles.models import Cycle


class Booking(BaseModel):
    """Booking model for cycle rentals"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateField(default=datetime.now)
    pickup_time = models.TimeField()
    dropoff_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    payment_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('paid', 'Paid')], default='pending')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Booking {self.id} - {self.user.username} - {self.cycle.title}"

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-booking_date', '-created_at']
        indexes = [
            models.Index(fields=['user', '-booking_date']),
            models.Index(fields=['cycle', 'status']),
        ]

    def calculate_duration(self):
        """Calculate booking duration in hours"""
        if self.dropoff_time:
            from datetime import combine, datetime as dt
            pickup = combine(self.booking_date, self.pickup_time)
            dropoff = combine(self.booking_date, self.dropoff_time)
            duration = (dropoff - pickup).total_seconds() / 3600
            return max(1, duration)  # Minimum 1 hour
        return 0

    def calculate_total_price(self):
        """Calculate total booking price"""
        duration = self.calculate_duration()
        self.total_price = duration * self.cycle.price_per_hour
        return self.total_price
