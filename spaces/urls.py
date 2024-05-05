#spaces/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MySpaceViewSet, FirePreventionTipsViewSet
from .views import create_user_fire_hazard, create_my_space, get_fire_hazard_assessment

router = DefaultRouter()
router.register(r'myspace', MySpaceViewSet, basename='myspace')
# router.register(r'mymap', MyMapViewSet, basename='usermap')
router.register(r'advice', FirePreventionTipsViewSet, basename='advice')

app_name = 'spaces'
urlpatterns = [
    path('', include(router.urls)),
    path('hazards/', create_user_fire_hazard, name='create_user_fire_hazard'),
    path('myspace/create', create_my_space, name='create-my-space'),
    path('get-vision-result/<int:my_space_detail_id>/', get_fire_hazard_assessment, name='get_fire_hazard_assessment'),
]
