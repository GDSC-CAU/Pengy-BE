from django.contrib import admin
from .models import MySpace, SpaceCategory, MySpaceDetail
from django.db.models import Count

# Inline admin for MySpaceDetail within MySpace admin
class MySpaceDetailInline(admin.TabularInline):
    model = MySpaceDetail
    extra = 1
    fields = ('nickname', 'thumbnail_image', 'count_user_fire_hazards')
    readonly_fields = ('count_user_fire_hazards',)

# Admin model for SpaceCategory
class SpaceCategoryAdmin(admin.ModelAdmin):
    list_display = ('categoryName',)
    list_filter = ('categoryName',)
    search_fields = ('categoryName',)
    ordering = ('categoryName',)

# Admin model for MySpace
class MySpaceAdmin(admin.ModelAdmin):
    list_display = ('spaceName', 'category', 'FirebaseUID_display', 'coordinates', 'address', 'related_hazards_count')
    list_filter = ('spaceName', 'category__categoryName', 'FirebaseUID__username')
    search_fields = ('spaceName', 'coordinates', 'category__categoryName', 'FirebaseUID__username')
    ordering = ('spaceName', 'coordinates')
    inlines = [MySpaceDetailInline]

    # Custom display function for FirebaseUID to show the username
    def FirebaseUID_display(self, obj):
        return obj.FirebaseUID.username if obj.FirebaseUID else ''
    FirebaseUID_display.short_description = "User"

    # Counting related hazards for each space
    def related_hazards_count(self, obj):
        return obj.myspacedetail_set.aggregate(Count('user_fire_hazards'))['user_fire_hazards__count']
    related_hazards_count.short_description = 'Number of Hazards'

# Register your models with their respective admin classes
admin.site.register(MySpaceDetail)
admin.site.register(SpaceCategory, SpaceCategoryAdmin)
admin.site.register(MySpace, MySpaceAdmin)
