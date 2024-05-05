from django.db import models
from spaces.models import MySpaceDetail

class FireHazardAssessment(models.Model):
    my_space_detail = models.ForeignKey(MySpaceDetail, on_delete=models.CASCADE, related_name='fire_hazard_assessments')
    place_or_object_description = models.CharField(max_length=255, blank=True)
    degree_of_fire_danger = models.IntegerField(default=0)
    identified_fire_hazards = models.TextField(blank=True)
    mitigation_measures = models.TextField(blank=True)
    additional_recommendations = models.TextField(blank=True)
    fact_check = models.TextField(blank=True)

    def __str__(self):
        return f"Fire Hazard Assessment for {self.my_space_detail.nickname} - Danger Level: {self.degree_of_fire_danger}"

    class Meta:
        verbose_name = "Fire Hazard Assessment"
        verbose_name_plural = "Fire Hazard Assessments"
