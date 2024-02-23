from django.db import models
from fireHazards.models import FireHazard


class EduContent(models.Model):
    # Linking to a specific FireHazard instance
    #firehazard id 참조
    fire_hazard = models.ForeignKey(FireHazard, on_delete=models.CASCADE)

    # JSON field to store Google news data related to the fire hazard
    google_news_data = models.JSONField()

    # fire hazard와 관련된 안전 사용 방법에 대한 문자열, 옵션
    fire_safety_instructions = models.TextField()

    # JSON field to store YouTube video links for fire prevention related to the fire hazard
    youtube_video_links = models.JSONField()

    # JSON field to store scholarly data related to the fire hazard
    scholarly_data = models.JSONField(null=True, blank=True)
    
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'EduContent for {self.fire_hazard}'

    class Meta:
        verbose_name = 'Educational Content'
        verbose_name_plural = 'Educational Contents'