#spaces/models.py
from django.db import models
from users.models import MyUser

class SpaceCategory(models.Model):
    categoryName = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.categoryName}"
    

#사용자와 1:N 관계
class MySpace(models.Model):
    FirebaseUID = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    category = models.ForeignKey(SpaceCategory, on_delete=models.CASCADE)
    spaceName = models.CharField(max_length=255)
    coordinates = models.CharField(max_length=255) #좌표값
    address = models.CharField(max_length=255) # 문자열로 된 주소값

    def __str__(self):
        return f"{self.spaceName} - {self.FirebaseUID}"
    
# 개별 체크리스트 항목 모델
class SpaceChecklist(models.Model):
    category = models.ForeignKey(SpaceCategory, on_delete=models.CASCADE, related_name="checklists")
    checklistItem = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.category.categoryName} - {self.checklistItem}"
    

# MySpace 인스턴스와 SpaceChecklist 인스턴스 간의 완료 상태를 추적하는 모델
class MySpaceChecklistStatus(models.Model):
    mySpace = models.ForeignKey(MySpace, on_delete=models.CASCADE, related_name="checklistStatuses")
    checklistItem = models.ForeignKey(SpaceChecklist, on_delete=models.CASCADE, related_name="status")
    isCompleted = models.BooleanField(default=False)

    def __str__(self):
        status = "Completed" if self.isCompleted else "Not Completed"
        return f"{self.checklistItem.checklistItem} - {status} for {self.mySpace.spaceName}"