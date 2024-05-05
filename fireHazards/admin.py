from django.contrib import admin
from .models import FireHazard, UserFireHazard

class FireHazardAdmin(admin.ModelAdmin):
    list_display = ('object',)
    list_filter = ('object',)
    search_fields = ('object',)
    ordering = ('object',)

class UserFireHazardAdmin(admin.ModelAdmin):
    list_display = ('my_space_detail_display', 'fire_hazard', 'thumbnail_image_display', 'nickname_display')
    list_filter = ('my_space_detail__my_space', 'fire_hazard__object')
    search_fields = ('my_space_detail__nickname', 'fire_hazard__object')
    ordering = ('my_space_detail', 'fire_hazard')

    def my_space_detail_display(self, obj):
        return obj.my_space_detail.my_space.spaceName
    my_space_detail_display.short_description = 'My Space'

    def thumbnail_image_display(self, obj):
        return obj.my_space_detail.thumbnail_image.url if obj.my_space_detail.thumbnail_image else "No image"
    thumbnail_image_display.short_description = 'Thumbnail Image'

    def nickname_display(self, obj):
        return obj.my_space_detail.nickname
    nickname_display.short_description = 'Nickname'

admin.site.register(FireHazard, FireHazardAdmin)
admin.site.register(UserFireHazard, UserFireHazardAdmin)
