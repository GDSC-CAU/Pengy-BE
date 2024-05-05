from rest_framework import viewsets
from rest_framework.response import Response
from fireHazards.models import FireHazard
from .models import EduContent
from .serializers import EduContentSerializer
from fireHazards.serializers import FireHazardSerializer # Assuming you have an EduContentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .utils import update_edu_content, save_edu_content_with_str
from rest_framework import status
from django.shortcuts import get_object_or_404

class FireHazardEducationViewSet(viewsets.ViewSet):
    """
    [Documentation]
    """
    # permission_classes = [IsAuthenticated]
    def retrieve(self, request, pk=None):
        fire_hazard = get_object_or_404(FireHazard, pk=pk)
        serialized_fire_hazard = FireHazardSerializer(fire_hazard).data

        # Try fetching EduContent with a more defensive approach
        try:
            edu_content = EduContent.objects.get(fire_hazard=fire_hazard)
            serialized_edu_content = EduContentSerializer(edu_content).data
        except EduContent.DoesNotExist:
            return Response({'error': 'Educational content for the specified FireHazard does not exist'}, status=404)

        response_data = {
            'fire_hazard': serialized_fire_hazard,
            'google_news_data': serialized_edu_content['google_news_data'],
            'youtube_video_links': serialized_edu_content['youtube_video_links'],
            'scholarly_data': serialized_edu_content['scholarly_data']
        }
        
        return Response(response_data)

    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def update_contents(self, request):
        fire_hazards = FireHazard.objects.all()
        for hazard in fire_hazards:
            update_edu_content(hazard.id)
        return Response({'status': 'Successfully updated educational content for all fire hazards'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated], url_path='fetch-edu-content/(?P<slug>[^/.]+)')
    def fetch_edu_content(self, request, slug=None):
        """
        Fetch educational content based on the fire hazard string descriptor.
        """
        try:
            # Here slug would be the string identifier for the FireHazard
            edu_content_data = save_edu_content_with_str(slug)

            if edu_content_data is None:
                return Response({'error': 'No educational content found for the given identifier'}, status=status.HTTP_404_NOT_FOUND)

            return Response(edu_content_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)