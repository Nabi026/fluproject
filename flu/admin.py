from django.contrib import admin
from .models import (
    ContactMessage
)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 
        'email', 
        'subject', 
        'is_read', 
        'replied', 
        'created_at'
    ]
    list_filter = ['subject', 'is_read', 'replied', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'message']
    list_editable = ['is_read', 'replied']
    readonly_fields = ['first_name', 'last_name', 'email', 'phone', 'subject', 'message', 'created_at', 'updated_at']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Message Details', {
            'fields': ('subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'replied', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Don't allow adding messages through admin (only through contact form)
        return False
    
    actions = ['mark_as_read', 'mark_as_replied']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} message(s) marked as read.')
    mark_as_read.short_description = 'Mark selected messages as read'
    
    def mark_as_replied(self, request, queryset):
        updated = queryset.update(replied=True)
        self.message_user(request, f'{updated} message(s) marked as replied.')
    mark_as_replied.short_description = 'Mark selected messages as replied'


# Customize admin site header and title
admin.site.site_header = 'Flu Prevention Admin'
admin.site.site_title = 'Flu Admin'
admin.site.index_title = 'Flu Website Management'