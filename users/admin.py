# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, Device

admin.site.register(MyUser, UserAdmin)
#myuser가 바로 보이게 하기
class MyUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'FirebaseUID', 'is_staff', 'is_active')
    list_filter = ('username', 'email', 'FirebaseUID', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'FirebaseUID', 'is_staff', 'is_active')
    ordering = ('username', 'email', 'FirebaseUID', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'FirebaseUID', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'FirebaseUID', 'password1', 'password2')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    filter_horizontal = ()

# Device 모델을 admin 페이지에서 보이게 하기
class MyDeviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'fcmToken')
    list_filter = ('user', 'fcmToken')
    search_fields = ('user', 'fcmToken')
    ordering = ('user', 'fcmToken')

admin.site.register(Device, MyDeviceAdmin)
