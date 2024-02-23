from django.contrib import admin
from .models import EduContent

class EduContentAdmin(admin.ModelAdmin):
    # Displaying fields in the list view
    list_display = ('fire_hazard', 'created_at', 'updated_at')
    
    # Enabling search functionality
    search_fields = ['fire_hazard__name', 'google_news_data', 'fire_safety_instructions', 'youtube_video_links', 'scholarly_data']
    
    # Enabling filter functionality
    list_filter = ('created_at', 'updated_at')
    
    # Customizing how individual pages look
    fieldsets = (
        ('Fire Hazard Information', {
            'fields': ('fire_hazard', )
        }),
        ('Educational Data', {
            'fields': ('google_news_data', 'fire_safety_instructions', 'youtube_video_links', 'scholarly_data')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    # Set readonly fields
    readonly_fields = ('created_at', 'updated_at')
    
admin.site.register(EduContent, EduContentAdmin)
