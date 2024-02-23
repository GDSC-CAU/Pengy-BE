#spaces/views.py
from users.models import MyUser
from .models import MySpace, MyUser
from .serializers import MySpaceSerializer
from fireHazards.serializers import UserFireHazardSerializer
from fireHazards.models import UserFireHazard, UserFireHazard
from .utils import generate_fire_prevention_tips, upload_image

from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from django.contrib.auth import login

import firebase_admin
from firebase_admin import auth, exceptions

from .models import SpaceChecklist, MySpaceChecklistStatus
from .serializers import MySpaceChecklistStatusSerializer
from django.http import Http404



class MySpaceViewSet(viewsets.ModelViewSet):
    serializer_class = MySpaceSerializer

    # 사용자 myspace에 등록된 화재위험물을 반환
    @action(detail=False, methods=['get'], url_path='(?P<space_id>\d+)')
    def fire_hazards(self, request, space_id=None):
        
        myspace = get_object_or_404(MySpace, id=space_id)
        
        # 현재 로그인된 사용자의 FirebaseUID와 MySpace 인스턴스의 FirebaseUID가 일치하는지 확인
        if myspace.FirebaseUID != request.user:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        # 해당 MySpace 인스턴스와 연결된 UserFireHazard 객체를 조회
        user_fire_hazards = UserFireHazard.objects.filter(my_space=myspace)
        
        # UserFireHazardSerializer를 사용하여 데이터를 직렬화하고 반환
        serializer = UserFireHazardSerializer(user_fire_hazards, many=True)
        return Response(serializer.data)
    
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
        
@api_view(['POST'])
def create_my_space(request):
    """Create a MySpace instance for authenticated users based on Firebase ID token."""
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

            if space_serializer.is_valid():
                space_serializer.save(FirebaseUID=user)
                print(f"Space created for user {user.username}")

                # 만든 공간에 대해서 체크리스트 항목을 생성합니다. 
                category_id = mutable_data.get('category')
                my_space_instance = MySpace.objects.get(FirebaseUID=user, spaceName=mutable_data.get('spaceName'))
                checklist_items = SpaceChecklist.objects.filter(category_id=category_id)
                checklist_statuses = [
                    MySpaceChecklistStatus(mySpace=my_space_instance, checklistItem=item, isCompleted=False)
                    for item in checklist_items
                ]           
                MySpaceChecklistStatus.objects.bulk_create(checklist_statuses)
                print(f"Checklist items created for {my_space_instance.spaceName}")

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
    """Create a UserFireHazard instance for authenticated users based on Firebase ID token."""
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


# 더이상 안쓰이는 api인듯 하다.
# class MyMapViewSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = MyMapSerializer

#     def get_queryset(self):
#         # 현재 로그인된 사용자의 FirebaseUID를 기반으로 쿼리셋을 반환합니다.
#         return MySpace.objects.filter(FirebaseUID=self.request.user).only('coordinates', 'spaceName')

    
# utils에서 generate_fire_prevention_tips 함수를 import한다. 생성형 api로 사용자 공간과 화재 물품에 대해서 맞춤형 조언을 주는 api.
class FirePreventionTipsViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'], url_path='(?P<space_id>\d+)')
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
def get_myspace_checklist_status(request, myspace_id):
    """
    Retrieves the checklist completion status for the specified MySpace instance.
    """
    try:
        myspace = get_object_or_404(MySpace, id=myspace_id)
        # # Ensure the request user is the owner of the MySpace instance
        # if myspace.FirebaseUID != request.user:
        #     return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        
        # 해당 MySpace 인스턴스와 연결된 모든 MySpaceChecklistStatus 인스턴스를 가져옵니다.
        checklist_statuses = MySpaceChecklistStatus.objects.filter(mySpace=myspace)
        print(checklist_statuses)
        # MySpaceChecklistStatusSerializer 시리얼라이저
        serializer = MySpaceChecklistStatusSerializer(checklist_statuses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except MySpace.DoesNotExist:
        print(f'MySpace with ID {myspace_id} does not exist.')
        return Response({"error": "MySpace not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"An error occurred while retrieving the checklist: {e}")
        return Response({"error": f"An error occurred while retrieving the checklist: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def update_checklist_status(request, myspace_id):
    """
    Updates the completion status of a checklist item for the specified MySpace instance.
    """
    # try:
    #     authorization_header = request.headers.get('Authorization')
    #     id_token = authorization_header.split(' ')[1]
    # except Exception as e:
    #     print("Authorization header is missing or invalid")
    #     return Response({'error': 'Authorization header is missing or invalid'}, status=status.HTTP_401_UNAUTHORIZED)

    # try:
    #     auth.verify_id_token(id_token)
    # except exceptions.FirebaseError as ex:
    #     error_message = f'Firebase error: {ex.message}' if hasattr(ex, 'message') else 'Firebase authentication error'
    #     print(error_message)
    #     return Response({'error': error_message}, status=status.HTTP_401_UNAUTHORIZED)
    
    update_results = []
    for item in request.data:
        try:
            checklist_item_id = item.get('checklist_item_id')
            is_completed = item.get('is_completed')
            
            # 해당 MySpaceChecklistStatus 인스턴스를 가져온다
            checklist_status = MySpaceChecklistStatus.objects.get(
                mySpace_id=myspace_id,
                checklistItem_id=checklist_item_id,
            )
            checklist_status.isCompleted = is_completed
            checklist_status.save()

            update_results.append({"checklist_item_id": checklist_item_id, "status": "success"})
            print(f"Checklist status updated for item ID {checklist_item_id} in MySpace ID {myspace_id}")

        except Exception as e:
            print(f"An error occurred while updating the checklist status for item ID {checklist_item_id}: {e}")
            update_results.append({"checklist_item_id": checklist_item_id, "status": "error", "message": str(e)})
    
    # 모든 항목의 업데이트 결과를 반환
    return Response({"status": "success", "update_results": update_results}, status=status.HTTP_200_OK)
        