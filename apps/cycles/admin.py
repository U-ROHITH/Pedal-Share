from django.contrib import admin
from apps.cycles.models import Cycle


@admin.register(Cycle)
class CycleAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'cycle_type', 'price_per_hour', 'is_available', 'rating', 'created_at']
    list_filter = ['cycle_type', 'is_available', 'is_active', 'created_at']
    search_fields = ['title', 'owner__username', 'location', 'registration_number']
    readonly_fields = ['created_at', 'updated_at', 'total_bookings', 'rating']
    
    fieldsets = (
        ('Basic Info', {'fields': ('owner', 'title', 'description')}),
        ('Details', {'fields': ('cycle_type', 'color', 'registration_number')}),
        ('Pricing & Location', {'fields': ('price_per_hour', 'location', 'latitude', 'longitude')}),
        ('Availability', {'fields': ('available_from', 'available_until', 'is_available')}),
        ('Image', {'fields': ('image',)}),
        ('Performance', {'fields': ('rating', 'total_bookings')}),
        ('Status', {'fields': ('is_active',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
