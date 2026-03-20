from django.contrib import admin
from apps.users.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'phone', 'wallet_balance', 'is_verified', 'created_at']
    list_filter = ['is_verified', 'created_at', 'is_active']
    search_fields = ['user__username', 'user__email', 'full_name', 'phone']
    readonly_fields = ['created_at', 'updated_at', 'total_rides', 'total_earnings']
    
    fieldsets = (
        ('User Info', {'fields': ('user',)}),
        ('Personal', {'fields': ('full_name', 'phone', 'avatar', 'bio')}),
        ('Wallet', {'fields': ('wallet_balance',)}),
        ('Statistics', {'fields': ('total_rides', 'total_earnings', 'rating')}),
        ('Verification', {'fields': ('is_verified',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
