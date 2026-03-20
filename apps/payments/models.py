from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
from apps.core.models import BaseModel
from apps.bookings.models import Booking


class Transaction(BaseModel):
    """Transaction model for payment tracking"""
    TRANSACTION_TYPES = [
        ('wallet_topup', 'Wallet Top-up'),
        ('booking_payment', 'Booking Payment'),
        ('refund', 'Refund'),
        ('earnings', 'Earnings'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200)
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    balance_before = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    balance_after = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    reference_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('success', 'Success'), ('failed', 'Failed'), ('pending', 'Pending')], default='pending')

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.user.username} - ₹{self.amount}"

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status', 'created_at']),
        ]
