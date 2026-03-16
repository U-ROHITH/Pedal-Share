from django.contrib import admin
from apps.bookings.models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'cycle', 'booking_date', 'status', 'payment_status', 'total_price']
    list_filter = ['status', 'payment_status', 'booking_date', 'created_at']
    search_fields = ['user__username', 'cycle__title']
    readonly_fields = ['created_at', 'updated_at', 'total_price']
    
    fieldsets = (
        ('Booking Info', {'fields': ('user', 'cycle')}),
        ('Dates & Times', {'fields': ('booking_date', 'pickup_time', 'dropoff_time')}),
        ('Status', {'fields': ('status', 'payment_status')}),
        ('Pricing', {'fields': ('total_price',)}),
        ('Notes', {'fields': ('notes',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
