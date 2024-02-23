from django.urls import path
from .views import signUp, signIn

app_name = 'users'
urlpatterns = [
    path('signUp/', signUp, name='signUp'),
    path('signIn/', signIn, name='signIn'),
]
