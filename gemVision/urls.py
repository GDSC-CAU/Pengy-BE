from django.urls import path
from .views import GenerateVisionResultView

app_name = 'gemVision'

urlpatterns = [
    path('generate-vision-result/', GenerateVisionResultView.as_view(), name='generate_vision_result'),
]
