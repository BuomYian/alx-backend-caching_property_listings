from django.contrib import admin
from .models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'location', 'created_at')
    list_filter = ('location', 'created_at', 'price')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description')
        }),
        ('Property Details', {
            'fields': ('price', 'location')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
