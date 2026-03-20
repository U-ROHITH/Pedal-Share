from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from apps.core.models import BaseModel


class Cycle(BaseModel):
    """Cycle model for sharing platform"""
    TYPE_CHOICES = [
        ('regular', 'Regular'),
        ('electric', 'Electric'),
        ('mountain', 'Mountain'),
        ('hybrid', 'Hybrid'),
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_cycles')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    cycle_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='regular')
    color = models.CharField(max_length=50, default='Black')
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('20.00'))
    location = models.CharField(max_length=200)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    available_from = models.TimeField()
    available_until = models.TimeField()
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='cycles/', blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=Decimal('4.5'))
    total_bookings = models.PositiveIntegerField(default=0)
    registration_number = models.CharField(max_length=50, blank=True, null=True, unique=True)

    def __str__(self):
        return f"{self.title} by {self.owner.username}"

    class Meta:
        verbose_name = 'Cycle'
        verbose_name_plural = 'Cycles'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['owner', '-created_at']),
            models.Index(fields=['is_available', 'price_per_hour']),
        ]
