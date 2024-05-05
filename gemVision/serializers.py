from rest_framework import serializers
from .models import FireHazardAssessment

class SpaceTemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FireHazardAssessment
        fields = ['degree_of_fire_danger']


class FireHazardAssessmentSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = FireHazardAssessment
        fields = [
            'id',
            'my_space_detail',
            'nickname',  # 이 필드를 fields 리스트에 추가
            'place_or_object_description',
            'degree_of_fire_danger',
            'identified_fire_hazards',
            'mitigation_measures',
            'additional_recommendations',
            'fact_check'
        ]

    def get_nickname(self, obj):
        return obj.my_space_detail.nickname
