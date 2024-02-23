# fireHazards/serializers.py

from rest_framework import serializers
from .models import FireHazard, UserFireHazard

class FireHazardSerializer(serializers.ModelSerializer):
    class Meta:
        model = FireHazard
        fields = '__all__'  # 모든 필드를 포함시키거나, 필요한 필드만 명시할 수 있습니다.

class UserFireHazardSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFireHazard
        fields = '__all__'  # 모든 필드를 포함시키거나, 필요한 필드만 명시할 수 있습니다.
