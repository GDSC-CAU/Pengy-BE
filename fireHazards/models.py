#fireHazards/models.py
from django.db import models
from spaces.models import MySpace

class HazardCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

#서버에서 미리 지정한 DB의 화재위험물
class FireHazard(models.Model):
    hazard_category = models.ForeignKey(HazardCategory, on_delete=models.CASCADE)  # 카테고리 모델 참조
    object = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.hazard_category.name} - {self.object}"

#사용자의 화재위험물
#MySpace와 1:N 관계
class UserFireHazard(models.Model):
    my_space = models.ForeignKey(MySpace, on_delete=models.CASCADE)
    fire_hazard = models.ForeignKey(FireHazard, on_delete=models.CASCADE)
    thumbnail_image = models.ImageField(upload_to='fire_hazards_thumbnails/', blank=True, null=True) 
    nickname = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nickname} - {self.fire_hazard}"
