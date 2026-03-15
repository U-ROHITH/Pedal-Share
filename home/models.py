from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal


class UserProfile(models.Model):
    user           = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name      = models.CharField(max_length=150, blank=True)
    phone          = models.CharField(max_length=15, blank=True)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('500.00'))

    def __str__(self):
        return f"{self.user.username} — ₹{self.wallet_balance}"


class Cycle(models.Model):
    TYPE_CHOICES = [
        ('regular',  'Regular'),
        ('electric', 'Electric'),
        ('mountain', 'Mountain'),
        ('hybrid',   'Hybrid'),
    ]
    owner           = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cycles')
    owner_name      = models.CharField(max_length=100)
    avatar_color    = models.CharField(max_length=100, default='linear-gradient(135deg,#1ABC9C,#16A085)')
    title           = models.CharField(max_length=100)
    cycle_type      = models.CharField(max_length=20, choices=TYPE_CHOICES, default='regular')
    color           = models.CharField(max_length=50, default='Black')
    price_per_hour  = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('20.00'))
    location        = models.CharField(max_length=200)
    available_from  = models.TimeField()
    available_until = models.TimeField()
    is_available    = models.BooleanField(default=True)
    rating          = models.DecimalField(max_digits=3, decimal_places=1, default=Decimal('4.5'))
    total_rides     = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} by {self.owner_name}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('active',    'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    cycle        = models.ForeignKey(Cycle, on_delete=models.CASCADE, related_name='bookings')
    hours        = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    booked_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-booked_at']

    def __str__(self):
        return f"Booking #{self.pk} — {self.user.username} → {self.cycle.title}"


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('credit', 'Credit'),
        ('debit',  'Debit'),
    ]
    user             = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    amount           = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    description      = models.CharField(max_length=255)
    created_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_type} ₹{self.amount} — {self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
