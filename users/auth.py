#users/auth.py
from django.contrib.auth.backends import ModelBackend
from .models import MyUser

class FirebaseBackend(ModelBackend):
    def authenticate(self, request, uid=None, **kwargs):
        try:
            user = MyUser.objects.get(FirebaseUID=uid)
            return user
        except MyUser.DoesNotExist:
            return None