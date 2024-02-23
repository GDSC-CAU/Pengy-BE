from django.urls import path, include
from .views import FireHazardEducationViewSet

app_name = 'eduContents'
urlpatterns = [
    path('get-contents/<int:pk>/', FireHazardEducationViewSet.as_view({'get': 'retrieve'}), name='get_contents'),
    path('update-contents/', FireHazardEducationViewSet.as_view({'post': 'update_contents'}), name='update_contents'),
]