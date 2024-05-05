from rest_framework import serializers
from .models import MySpace, SpaceCategory, MySpaceDetail
from users.models import MyUser

class SpaceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SpaceCategory
        fields = ['id', 'categoryName']

class MySpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MySpace
        fields = ['id', 'FirebaseUID', 'category', 'spaceName', 'coordinates', 'address'] 


class MySpaceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MySpaceDetail
        fields = '__all__'  # You might want to specify only certain fields

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'username', 'email'] # 여기서 필요한 필드를 지정합니다.


# 아마 안쓰는 것 같습니다
class MyMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = MySpace
        fields = ['coordinates', 'spaceName']

        
