# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, Device

class MyUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'get_firebase_uid', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email', 'firebase_uid')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'FirebaseUID', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'FirebaseUID', 'password1', 'password2')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    filter_horizontal = ()

    def get_firebase_uid(self, obj):
        return obj.FirebaseUID  # FirebaseUID 속성으로 수정

    get_firebase_uid.short_description = 'FirebaseUID'  # 필드 이름 설정

    get_firebase_uid.admin_order_field = 'firebase_uid'

admin.site.register(MyUser, MyUserAdmin)

class MyDeviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_fcm_token')
    list_filter = ('user__username',)

    def get_fcm_token(self, obj):
        return obj.fcmToken

    get_fcm_token.short_description = 'FCM Token'

admin.site.register(Device, MyDeviceAdmin)
