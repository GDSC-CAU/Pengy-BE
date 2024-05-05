# fireHazards/models.py
from django.db import models

class FireHazard(models.Model):
    object = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.object}"

class UserFireHazard(models.Model):
    my_space_detail = models.ForeignKey('spaces.MySpaceDetail', on_delete=models.CASCADE, related_name='user_fire_hazards')
    fire_hazard = models.ForeignKey(FireHazard, on_delete=models.CASCADE)
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.my_space_detail.nickname} - {self.fire_hazard}"
