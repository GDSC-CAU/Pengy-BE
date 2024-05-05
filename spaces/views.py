#spaces/views.py
from users.models import MyUser
from .models import MySpace, MyUser, MySpaceDetail
from .serializers import MySpaceSerializer, MySpaceDetailSerializer
from fireHazards.serializers import UserFireHazardSerializer
from fireHazards.models import UserFireHazard, UserFireHazard
from gemVision.serializers import SpaceTemperatureSerializer, FireHazardAssessmentSerializer
from gemVision.models import FireHazardAssessment
from django.db.models import Avg
from .utils import generate_fire_prevention_tips, upload_image

from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from django.contrib.auth import login

import firebase_admin
from firebase_admin import auth, exceptions

from django.http import Http404




class MySpaceViewSet(viewsets.ModelViewSet):
    serializer_class = MySpaceSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()  # 현재 로그인한 사용자의 MySpace 쿼리셋을 가져옴
        response_data = []

        for myspace in queryset:
            # Calculate the average degree_of_fire_danger
            average_fire_danger = self.get_average_temperature(myspace)

            # MySpace 데이터 시리얼라이즈
            space_serializer = MySpaceSerializer(myspace)

            # 응답 데이터에 각 공간의 정보와 평균 화재 위험도 추가
            space_data = space_serializer.data
            space_data['average_temperature'] = average_fire_danger
            response_data.append(space_data)

        return Response(response_data)  # 시리얼라이즈된 데이터와 평균 화재 위험도를 함께 반환

    @action(detail=False, methods=['get'], url_path='(?P<space_id>\\d+)')
    def fire_hazards(self, request, space_id=None):
        myspace = get_object_or_404(MySpace, id=space_id)
        
        # # Check if the current logged-in user's FirebaseUID matches the MySpace instance's FirebaseUID
        # if myspace.FirebaseUID != request.user.FirebaseUID:  # Make sure to access the correct attribute of request.user
        #     return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        # Retrieve MySpaceDetail instances related to the MySpace instance
        my_space_details = MySpaceDetail.objects.filter(my_space=myspace)

        # Calculate the average degree_of_fire_danger
        average_fire_danger = self.get_average_temperature(myspace)

        # Serialize the MySpaceDetail data
        space_detail_serializer = MySpaceDetailSerializer(my_space_details, many=True)

        # Add the average degree of fire danger to the response
        response_data = {
            'space_details': space_detail_serializer.data,
            'average_degree_of_fire_danger': average_fire_danger
        }
        
        return Response(response_data)
    
    # 사용자의 myspace
    def get_queryset(self):
        """
        This view returns a list of all the MySpace instances
        for the currently authenticated user.
        """
        try:
            #현재 로그인한 사용자의 FirebaseUID를 기반으로 쿼리셋을 반환합니다.
            user = self.request.user
        except MyUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        try: 
            
            return MySpace.objects.filter(FirebaseUID=user)
        except MySpace.DoesNotExist:
            return Response({'error': 'Space not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def get_average_temperature(self, myspace):
        my_space_details = MySpaceDetail.objects.filter(my_space=myspace)
        my_fire_hazard_assessments = FireHazardAssessment.objects.filter(my_space_detail__in=my_space_details)

        # degree_of_fire_danger 값들의 평균을 계산
        average_fire_danger = my_fire_hazard_assessments.aggregate(Avg('degree_of_fire_danger'))['degree_of_fire_danger__avg']
        if average_fire_danger is None:
            average_fire_danger = 0  # 평균 데이터가 없는 경우 0으로 설정
    
        return average_fire_danger
        

@api_view(['POST'])
def create_my_space(request):
    """Myspace 인스턴스를 새로 create하는 api."""
    authorization_header = request.headers.get('Authorization')
    if authorization_header and authorization_header.startswith('Bearer '):
        id_token = authorization_header.split(' ')[1]
    else:
        print("Authorization header is missing or invalid")
        return Response({'error': 'Authorization header is missing or invalid'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        # Verify the Firebase ID token
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']

        try:
            # Look up the user by their Firebase UID
            user = MyUser.objects.get(FirebaseUID=uid)

            # Perform Django login
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            # request.data는 불변이므로, 사본을 만들어 수정합니다.
            mutable_data = request.data.copy()
            mutable_data['FirebaseUID'] = user.id  # 사용자 인스턴스의 ID를 추가합니다.

            space_serializer = MySpaceSerializer(data=mutable_data)

            category_id = mutable_data.get('category')

            if space_serializer.is_valid():
                space_serializer.save(FirebaseUID=user)
                print(f"Space created for user {user.username}")

                category_id = mutable_data.get('category')
                my_space_instance = MySpace.objects.get(FirebaseUID=user, spaceName=mutable_data.get('spaceName'))

                return Response(space_serializer.data, status=status.HTTP_201_CREATED)
            else:
                print("serializer is not valid")
                print(space_serializer.errors) 
                return Response(space_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except MyUser.DoesNotExist:
            print(f'User with FirebaseUID {uid} does not exist.')
            return Response({'error': 'User does not exist. Please sign up.'}, status=status.HTTP_404_NOT_FOUND)
        
    except exceptions.FirebaseError as ex:
        error_message = f'Firebase error: {ex.message}' if hasattr(ex, 'message') else 'Firebase authentication error2'
        print(error_message)
        return Response({'error': error_message}, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['POST'])
def create_user_fire_hazard(request):
    """화재 위험 물품을 등록하는 api."""
    authorization_header = request.headers.get('Authorization')
    if authorization_header and authorization_header.startswith('Bearer '):
        id_token = authorization_header.split(' ')[1]  # Extract the actual token
    else:
        print("Authorization header is missing or invalid")
        return Response({'error': 'Authorization header is missing or invalid'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        # Verify the Firebase ID token
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']

        try:
            # Look up the user by their Firebase UID
            user = MyUser.objects.get(FirebaseUID=uid)

            # Perform Django login
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            # Process the POST request to create a UserFireHazard instance
            serializer = UserFireHazardSerializer(data=request.data)
            my_space_id = request.data.get('my_space')

            if serializer.is_valid():
                myspace = MySpace.objects.get(id=my_space_id)
                serializer.save(my_space=myspace)  # Assuming UserFireHazard has a 'user' field to link to MyUser
                user_fire_hazard = serializer.save(my_space=myspace)
                try:
                    image_file = request.FILES.get('thumbnail_image')
                    print(f"image file found : {image_file}")
                except:
                    image_file = None
                    print("No image file found")
                if image_file:
                    # 이미지 저장 함수를 호출하여 이미지 파일을 저장하고 URL을 받아옵니다.
                    image_url = upload_image(image_file, 'fire_hazard_thumbnails')
                    if image_url:
                        user_fire_hazard.thumbnail_image = image_url
                        user_fire_hazard.save()
                        print(f"Image uploaded successfully: {image_url}")
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        # 이미지 업로드 실패 처리
                        print("Failed to upload image")
                        return Response({'error': 'Failed to upload image'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            else:
                print("serializer is not valid")
                print(serializer.errors) 
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except MyUser.DoesNotExist:
            print(f'User with FirebaseUID {uid} does not exist.')
            return Response({'error': 'User does not exist. Please sign up.'}, status=status.HTTP_404_NOT_FOUND)
        
    except exceptions.FirebaseError as ex:
        error_message = f'Firebase error: {ex.message}' if hasattr(ex, 'message') else 'Firebase authentication error2'
        print(error_message)
        return Response({'error': error_message}, status=status.HTTP_401_UNAUTHORIZED)

    
class FirePreventionTipsViewSet(viewsets.ViewSet):
    """utils에서 generate_fire_prevention_tips 함수를 import한다. 생성형 api로 사용자 공간과 화재 물품에 대해서 맞춤형 조언을 주는 api"""
    @action(detail=False, methods=['get'], url_path='(?P<space_id>\\d+)')
    def advice(self, request, space_id=None):
        if space_id:
            # space_id를 사용하여 MySpace 인스턴스 조회
            try:
                my_space = MySpace.objects.get(id=space_id)
                space_category = my_space.category  # spaceName 추출
            except MySpace.DoesNotExist:
                return Response({'error': 'Space not found'}, status=status.HTTP_404_NOT_FOUND)
            
            user_fire_hazards = UserFireHazard.objects.filter(my_space_id=space_id)
            fire_items = [ufh.fire_hazard.object for ufh in user_fire_hazards]

            if fire_items:
                # space_name을 사용하여 맞춤형 조언 생성
                tips = generate_fire_prevention_tips(space_category, fire_items)
                return Response({'fire_prevention_tips': tips}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No fire hazards found for the given space'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Space ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
def get_fire_hazard_assessment(request, my_space_detail_id):
    try:
        my_space_detail = MySpaceDetail.objects.get(id=my_space_detail_id)
    except MySpaceDetail.DoesNotExist:
        return Response({'error': 'MySpaceDetail not found'}, status=status.HTTP_404_NOT_FOUND)

    fire_hazard_assessments = FireHazardAssessment.objects.filter(my_space_detail=my_space_detail)

    if not fire_hazard_assessments.exists():
        return Response({'error': 'No Fire Hazard Assessments found for the provided MySpaceDetail'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = FireHazardAssessmentSerializer(fire_hazard_assessments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)