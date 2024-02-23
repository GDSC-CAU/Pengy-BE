from django.contrib import admin
from .models import MySpace, SpaceCategory, SpaceChecklist, MySpaceChecklistStatus

# spaceCategory가 바로 보이게 하기
class SpaceCategoryAdmin(admin.ModelAdmin):
    list_display = ('categoryName',)
    list_filter = ('categoryName',)
    search_fields = ('categoryName',)
    ordering = ('categoryName',)

# mySpace가 바로 보이게 하기
class MySpaceAdmin(admin.ModelAdmin):
    list_display = ('spaceName', 'coordinates', 'category', 'FirebaseUID')
    list_filter = ('spaceName', 'coordinates', 'category', 'FirebaseUID')
    search_fields = ('spaceName', 'coordinates', 'category', 'FirebaseUID')
    ordering = ('spaceName', 'coordinates', 'category', 'FirebaseUID')

# spaceChecklist가 바로 보이게 하기
class SpaceChecklistAdmin(admin.ModelAdmin):
    list_display = ('category', 'checklistItem')
    list_filter = ('category', 'checklistItem')
    search_fields = ('category', 'checklistItem')
    ordering = ('category', 'checklistItem')

# mySpaceChecklistStatus가 바로 보이게 하기
class MySpaceChecklistStatusAdmin(admin.ModelAdmin):
    list_display = ('mySpace', 'checklistItem', 'isCompleted')
    list_filter = ('mySpace', 'checklistItem', 'isCompleted')
    search_fields = ('mySpace', 'checklistItem', 'isCompleted')
    ordering = ('mySpace', 'checklistItem', 'isCompleted')

admin.site.register(SpaceCategory, SpaceCategoryAdmin)
admin.site.register(MySpace, MySpaceAdmin)
admin.site.register(SpaceChecklist, SpaceChecklistAdmin)
admin.site.register(MySpaceChecklistStatus, MySpaceChecklistStatusAdmin)
