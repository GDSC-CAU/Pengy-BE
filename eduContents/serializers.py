from rest_framework import serializers
from .models import EduContent

class EduContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EduContent
        fields = ('google_news_data', 'youtube_video_links', 'scholarly_data')