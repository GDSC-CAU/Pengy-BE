# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class MyUser(AbstractUser):
    FirebaseUID = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.email

# 사용자가 여러 기기를 가질 수 있도록 1:N 관계로 설정
class Device(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name="유저", related_name="devices")
    fcmToken = models.CharField("FCM Token", max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.fcmToken[:25]}..."  # Shows a part of the FCM token for identification
