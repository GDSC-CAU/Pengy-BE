from rest_framework import serializers
from .models import MySpace, SpaceCategory, MySpaceChecklistStatus, SpaceChecklist
from users.serializers import MyUserSerializer

class SpaceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaceCategory
        fields = ['id', 'categoryName']

class SpaceChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaceChecklist
        fields = ['id', 'category', 'checklistItem']

class MySpaceSerializer(serializers.ModelSerializer):
    FirebaseUID = MyUserSerializer(read_only=True)
    category = SpaceCategorySerializer(read_only=True)
    checklist_completion = serializers.SerializerMethodField()

    class Meta:
        model = MySpace
        fields = ['id', 'FirebaseUID', 'category', 'spaceName', 'coordinates', 'address', 'checklist_completion']

    def get_checklist_completion(self, obj):
        total_count = SpaceChecklist.objects.filter(category=obj.category).count()
        completed_count = MySpaceChecklistStatus.objects.filter(mySpace=obj, isCompleted=True).count()
        return {
            "completed": completed_count,
            "total": total_count
        }
    
class MySpaceChecklistStatusSerializer(serializers.ModelSerializer):
    mySpace = MySpaceSerializer(read_only=True)
    checklistItem = SpaceChecklistSerializer(read_only=True)

    class Meta:
        model = MySpaceChecklistStatus
        fields = ['id', 'mySpace', 'checklistItem', 'isCompleted']

# class MyMapSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MySpace
#         fields = ['coordinates', 'spaceName']
