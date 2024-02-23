#spaces/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MySpaceViewSet, FirePreventionTipsViewSet
from .views import create_user_fire_hazard, create_my_space, get_myspace_checklist_status, update_checklist_status

router = DefaultRouter()
router.register(r'myspace', MySpaceViewSet, basename='myspace')
# router.register(r'mymap', MyMapViewSet, basename='usermap')
router.register(r'advice', FirePreventionTipsViewSet, basename='advice')

app_name = 'spaces'
urlpatterns = [
    path('', include(router.urls)),
    path('hazards/', create_user_fire_hazard, name='create_user_fire_hazard'),
    path('myspace/create', create_my_space, name='create-my-space'),
    path('myspace/<int:myspace_id>/get-checklist/', get_myspace_checklist_status, name='get-myspace-checklist-status'),
    path('myspace/<int:myspace_id>/update-checklist/', update_checklist_status, name='update-myspace-checklist-status'),
]
