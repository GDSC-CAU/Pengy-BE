# gemVision/views.py
from django.shortcuts import render
from rest_framework.views import APIView
from .utils import analyze_and_process_image_hazards
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from spaces.models import MySpaceDetail, MySpace
import os

from time import time
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
import os

class GenerateVisionResultView(APIView):
    def post(self, request, *args, **kwargs):
        start_time = time()  # Start timing here
        try:
            # #############################################################################
            # #test code
            # print("제미니 vision pro api 테스트용 코드실행 시작. 이미지, 닉네임, 장소 하드코딩되어서 들어감.")
            # image_file = 'gemVision/image5.jpg'  # Ensure this path points to a test image in your local setup
            # my_space_id = 5  # Assume a MySpace id for testing
            # nickname = 'TestNickname'  # Assume a nickname for testing
            # #############################################################################

            #############################################################################
            #production code 
            print("GEMINI Vision Pro API request 요청을 받았습니다.")
            image_file = request.FILES.get('image')
            nickname = request.data.get('nickname')
            my_space_id = request.data.get('my_space')
            #############################################################################

            my_space_instance, _ = MySpace.objects.get_or_create(id=my_space_id)
    
            my_space_detail_instance = create_my_space_detail_instance(my_space_instance, image_file, nickname)

            risk_result = analyze_and_process_image_hazards(request, image_file, my_space_detail_instance)

            print("Risk analysis completed.")
            end_time = time()  # End timing here
            duration = end_time - start_time  # Calculate duration
            print(f"post 요청 처리하는데 {duration:.2f} seconds. 걸렸음")
            
            return Response({
                "status": "success",
                "space_id": my_space_id,
                "space_detail_id": my_space_detail_instance.id,
                "Description" : risk_result['place_or_object_description'],
                "Degree of Fire Danger": risk_result['degree_of_fire_danger'],
                "Identified Fire Hazards": risk_result['identified_fire_hazards'],
                "Mitigation Measures": risk_result['mitigation_measures'],
                "Additional Recommendation": risk_result['additional_recommendations'],
                "Fact Check" : risk_result['fact_check'],
                "message": "MySpaceDetail created successfully",
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error processing the request: {str(e)}")
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

def create_my_space_detail_instance(my_space, image_file, nickname):
    my_space_detail = MySpaceDetail(
        my_space=my_space,
        thumbnail_image=image_file,
        nickname=nickname
    )
    my_space_detail.save()
    return my_space_detail


