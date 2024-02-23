from django.urls import path
from .views import send_periodic_notifications_api

app_name = 'notifications'
urlpatterns = [
    path('', send_periodic_notifications_api, name='send-notifications'),
]
