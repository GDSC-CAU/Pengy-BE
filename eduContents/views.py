from rest_framework import viewsets
from rest_framework.response import Response
from fireHazards.models import FireHazard
from .models import EduContent
from .serializers import EduContentSerializer
from fireHazards.serializers import FireHazardSerializer # Assuming you have an EduContentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .utils import update_edu_content
from rest_framework import status

class FireHazardEducationViewSet(viewsets.ViewSet):
    """
    [Documentation]
    """
    # permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        try:
            
            # Fetch the FireHazard instance
            fire_hazard = FireHazard.objects.get(id=pk)
            serialized_fire_hazard = FireHazardSerializer(fire_hazard).data

            # Fetch the related EduContent instance
            edu_content = EduContent.objects.get(fire_hazard=fire_hazard)
            serialized_edu_content = EduContentSerializer(edu_content).data  # Assuming serialization is done properly in EduContentSerializer
            
            response_data = {
                'fire_hazard': serialized_fire_hazard,
                'google_news_data': serialized_edu_content['google_news_data'],
                'youtube_video_links': serialized_edu_content['youtube_video_links'],
                'fire_safety_instructions': serialized_edu_content['fire_safety_instructions'],  # Text field
                'scholarly_data': serialized_edu_content['scholarly_data']  # JSON field
            }
            
            return Response(response_data)
        except FireHazard.DoesNotExist:
            return Response({'error': 'FireHazard not found'}, status=404)
        except EduContent.DoesNotExist:
            return Response({'error': 'Educational content for the specified FireHazard does not exist'}, status=404)

    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def update_contents(self, request):
        fire_hazards = FireHazard.objects.all()
        for hazard in fire_hazards:
            update_edu_content(hazard.id)
        return Response({'status': 'Successfully updated educational content for all fire hazards'}, status=status.HTTP_200_OK)

