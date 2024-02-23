# fireHazards 앱의 admin.py
from django.contrib import admin
from .models import FireHazard, UserFireHazard, HazardCategory

admin.site.register(HazardCategory)
admin.site.register(FireHazard)
admin.site.register(UserFireHazard)

#hazrdCategory가 바로 보이게 하기
class HazardCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

#fireHazard가 바로 보이게 하기
class FireHazardAdmin(admin.ModelAdmin):
    list_display = ('hazard_category', 'object')
    list_filter = ('hazard_category', 'object')
    search_fields = ('hazard_category', 'object')
    ordering = ('hazard_category', 'object')

#userFireHazard가 바로 보이게 하기
class UserFireHazardAdmin(admin.ModelAdmin):
    list_display = ('my_space', 'fire_hazard', 'thumbnail_image', 'nickname', 'capture_time')
    list_filter = ('my_space', 'fire_hazard', 'thumbnail_image', 'nickname', 'capture_time')
    search_fields = ('my_space', 'fire_hazard', 'thumbnail_image', 'nickname', 'capture_time')
    ordering = ('my_space', 'fire_hazard', 'thumbnail_image', 'nickname', 'capture_time')