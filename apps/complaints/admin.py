from django.contrib import admin
from apps.complaints.models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'category', 'subject', 'status', 'priority', 'created_at']
    list_filter = ['category', 'status', 'priority', 'created_at']
    search_fields = ['user__username', 'subject', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User & Details', {'fields': ('user', 'category', 'subject')}),
        ('Description', {'fields': ('description',)}),
        ('Related', {'fields': ('cycle', 'booking')}),
        ('Status', {'fields': ('status', 'priority', 'assigned_to')}),
        ('Resolution', {'fields': ('resolution',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
