from django.contrib import admin
from apps.payments.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'transaction_type', 'amount', 'status', 'created_at']
    list_filter = ['transaction_type', 'status', 'created_at']
    search_fields = ['user__username', 'description', 'reference_id']
    readonly_fields = ['created_at', 'updated_at', 'balance_before', 'balance_after']
    
    fieldsets = (
        ('User & Type', {'fields': ('user', 'transaction_type')}),
        ('Amount', {'fields': ('amount', 'balance_before', 'balance_after')}),
        ('Details', {'fields': ('description', 'booking', 'reference_id')}),
        ('Status', {'fields': ('status',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
