# spaces/models.py
from django.db import models
from users.models import MyUser

class SpaceCategory(models.Model):
    categoryName = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.categoryName}"

class MySpace(models.Model):
    FirebaseUID = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    category = models.ForeignKey(SpaceCategory, on_delete=models.CASCADE)
    spaceName = models.CharField(max_length=255)
    coordinates = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.spaceName} - {self.FirebaseUID}"

class MySpaceDetail(models.Model):
    my_space = models.ForeignKey(MySpace, on_delete=models.CASCADE)
    thumbnail_image = models.ImageField(upload_to='fire_hazards_thumbnails/', blank=True, null=True)
    nickname = models.CharField(max_length=255, null=True, blank=True)

    def count_user_fire_hazards(self):
        return self.user_fire_hazards.count()

    count_user_fire_hazards.short_description = "Number of Related Hazards"
