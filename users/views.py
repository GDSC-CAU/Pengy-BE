#users/views.py
from django.http import JsonResponse
from firebase_admin import auth, exceptions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED, HTTP_200_OK, HTTP_400_BAD_REQUEST
from .models import MyUser, Device
from django.contrib.auth import login
from quizzes.models import UserScore



@api_view(['POST'])
def signUp(request):
    """Register a new user using their Google account via Firebase."""
    # Authorization 헤더에서 Bearer 토큰을 추출합니다.
    authorization_header = request.headers.get('Authorization')
    if authorization_header and authorization_header.startswith('Bearer '):
        # 'Bearer '를 제거하여 실제 토큰 값을 가져옵니다.
        id_token = authorization_header[7:]
    else:
        # Authorization 헤더가 없거나 Bearer 토큰 형식이 아닌 경우 에러를 반환합니다.
        return JsonResponse({'error': 'Authorization header is missing or invalid'}, status=HTTP_401_UNAUTHORIZED)

    try:
        # Firebase ID 토큰을 검증합니다.
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        email = decoded_token.get('email')
        username = request.data.get('name')

        # UID와 이메일을 사용하여 새 사용자를 생성하거나 기존 사용자를 가져옵니다.
        user, created = MyUser.objects.get_or_create(FirebaseUID=uid, defaults={'username': username, 'email': email})

        # user_score 테이블에 사용자를 추가합니다.
        user_score, created = UserScore.objects.get_or_create(user=user, defaults={'fish_score': 0})

        if created:
            # 새 사용자가 성공적으로 생성된 경우
            return JsonResponse({'message': 'User registered successfully with Google.'}, status=HTTP_200_OK)
        else:
            # 사용자가 이미 존재하는 경우
            return JsonResponse({'error': 'User already exists.'}, status=HTTP_400_BAD_REQUEST)

    except exceptions.FirebaseError as ex:
        # Firebase 관련 오류 처리
        error_message = f'Firebase error: {ex.message}' if hasattr(ex, 'message') else 'Firebase authentication error'
        print(error_message)
        return JsonResponse({'error': error_message}, status=HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
def signIn(request):
    """Verify the user's Firebase ID token from Authorization header and attempt to log them in."""
    # Authorization 헤더에서 Bearer 토큰을 추출합니다.
    authorization_header = request.headers.get('Authorization')
    if authorization_header and authorization_header.startswith('Bearer '):
        id_token = authorization_header[7:]  # 'Bearer '를 제거하여 실제 토큰 값을 가져옵니다.
    else:
        return Response({'error': 'Authorization header is missing or invalid'}, status=HTTP_401_UNAUTHORIZED)

    try:
        # Firebase ID 토큰을 검증합니다.
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']

        try:
            # UID를 사용하여 사용자를 조회합니다.
            user = MyUser.objects.get(FirebaseUID=uid)
      # 로그인 처리를 유지합니다.
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # Backend 명시
        
            # 사용자를 로그인 처리합니다.
            print(f'User {user.email} logged in successfully')

            # 여기서 FCM 토큰을 업데이트합니다. (파이어베이스 클라우드 메시징을 위한 것)
            #클라이언트 요청에서 FCM 토큰을 가져옵니다.

            fcm_token = request.data.get('fcmToken')

            if fcm_token:
                
                # Device 모델을 사용하여 FCM 토큰을 업데이트하거나 새 기기를 등록합니다.
                Device.objects.update_or_create(user=user, fcmToken=fcm_token)

            return Response({
                'uid': user.FirebaseUID,
                'email': user.email,
                'message': 'User logged in successfully'
            }, status=HTTP_200_OK)
        except MyUser.DoesNotExist:
            return Response({'error': 'User does not exist. Please sign up.'}, status=HTTP_404_NOT_FOUND)

    except exceptions.FirebaseError as ex:
        error_message = f'Firebase error: {ex.message}' if hasattr(ex, 'message') else 'Firebase authentication error'
        return Response({'error': error_message}, status=HTTP_401_UNAUTHORIZED)