from rest_framework import views, status
from rest_framework.response import Response
from fireHazards.models import UserFireHazard
from .serializers import UserFireHazardSerializer
from spaces.models import MySpaceDetail
from django.shortcuts import get_object_or_404

class MySpaceDetailFireHazardsView(views.APIView):
    """
    Retrieve a list of fire hazards associated with a specific MySpaceDetail instance.
    """

    def get(self, request, id):
        try:
            my_space_detail = MySpaceDetail.objects.get(id=id)
        except MySpaceDetail.DoesNotExist:
            return Response({"error": "MySpaceDetail not found"}, status=status.HTTP_404_NOT_FOUND)

        # Fetching all user fire hazards related to the given MySpaceDetail
        user_fire_hazards = UserFireHazard.objects.filter(my_space_detail=my_space_detail)

        # Serializing the data
        serializer = UserFireHazardSerializer(user_fire_hazards, many=True)
        return Response(serializer.data)


class UpdateCheckView(views.APIView):
    """
    View to update the 'is_checked' status of a UserFireHazard instance.
    """

    def post(self, request):
        # For development testing (hard-coded)
        # hazard_id = 40

        # For production use
        hazard_id = request.data.get('id')

        # Retrieving 'is_checked' as a boolean. Defaulting to True if not provided.
        is_checked = request.data.get('is_checked', True)

        if hazard_id is None:
            return Response({"error": "Missing 'id' parameter"}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the specific UserFireHazard object, or return a 404 if not found
        user_fire_hazard = get_object_or_404(UserFireHazard, id=hazard_id)

        # Update the 'is_checked' status
        user_fire_hazard.is_checked = is_checked
        user_fire_hazard.save()

        # Serialize the updated object to return it in the response
        serializer = UserFireHazardSerializer(user_fire_hazard)
        return Response(serializer.data, status=status.HTTP_200_OK)
