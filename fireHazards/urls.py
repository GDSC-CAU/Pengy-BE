from django.urls import path
from .views import MySpaceDetailFireHazardsView, UpdateCheckView

app_name = 'fireHazards'

urlpatterns = [
    path('myspace_detail/<int:id>/', MySpaceDetailFireHazardsView.as_view(), name='myspace-detail-fire-hazards'),
    path('update-check/', UpdateCheckView.as_view(), name='update-check')
]
