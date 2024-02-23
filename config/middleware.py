# #config/middleware.py
# from users.models import MyUser
# from django.contrib.auth.middleware import AuthenticationMiddleware
# from django.http import HttpResponseForbidden
# from firebase_admin import auth, exceptions
# import firebase_admin
# import logging
# from django.contrib.auth import login
# from django.views.decorators.csrf import csrf_exempt
# from django.http import HttpResponse

# logger = logging.getLogger(__name__)

# # Firebase Admin SDK 초기화 (필요한 경우)
# if not firebase_admin._apps:
#     firebase_admin.initialize_app()

# #csrf_exempt 데코레이터를 추가합니다
# @csrf_exempt
# class FirebaseAuthenticationMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # 관리자 페이지, 회원가입, 로그인 페이지는 미들웨어를 적용하지 않음
#         if request.path.startswith('/admin/') or request.path.startswith('/users/signUp') or request.path.startswith('/users/signIn') :
#             response = self.get_response(request)
#             print("준형입니다.")
#             return response
        
#         #request 유저의 권한이 superuser면 미들웨어 적용하지 않는다
#         if request.user.is_superuser:
#             response = self.get_response(request)
#             return response

#         authorization_header = request.headers.get('Authorization')
#         if authorization_header:
#             try:
#                 token_type, token = authorization_header.split(' ', 1)
#                 print(token_type, token)

#                 if token_type.lower() == 'bearer':
#                     decoded_token = auth.verify_id_token(token)
#                     uid = decoded_token.get('uid')
#                     user = MyUser.objects.get(FirebaseUID=uid)

#                     # Django의 login 함수를 사용하여 사용자 세션을 시작합니다.
#                     login(request, user, backend='django.contrib.auth.backends.ModelBackend') #이게 있어야 일단 get 되는듯
#                     #login(request, user) #이게 있어야 일단 get 되는듯
#                     request.user = user
#                     # 요청 처리 로직 후
#                 else:
#                     return HttpResponseForbidden('Authorization header is not of type Bearer')
#             except (ValueError, auth.InvalidIdTokenError, exceptions.FirebaseError) as e:
#                 return HttpResponseForbidden('Invalid token or Firebase authentication error')
#         else:
#             return HttpResponseForbidden('No Authorization header provided')
        


#         response = self.get_response(request)
#         # response = HttpResponse("OK", status=200)
#         return response


from django.http import HttpResponseForbidden
from firebase_admin import auth, exceptions
import firebase_admin
import logging
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from users.models import MyUser

logger = logging.getLogger(__name__)

# Firebase Admin SDK 초기화 (필요한 경우)
if not firebase_admin._apps:
    firebase_admin.initialize_app()

# @csrf_exempt
class FirebaseAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 관리자 페이지, 회원가입, 로그인 페이지는 미들웨어를 적용하지 않음
        if request.path.startswith('/admin/') or request.path.startswith('/users/signUp') or request.path.startswith('/users/signIn'):
            return self.get_response(request)
        
        #post 요청에 대해서는 자체 미들웨어
        if (request.path.startswith('/api/spaces/hazards') or
            request.path.startswith('/api/spaces/myspace/create') or
            request.path.startswith('/api/quizzes/update-score') or
            request.path.startswith('/api/spaces/myspace/<int:myspace_id>/update-checklist/')):
            print("post 요청입니다.")
            return self.get_response(request)
        
        if request.user.is_superuser:
            return self.get_response(request)

        authorization_header = request.headers.get('Authorization')
        if authorization_header:
            try:
                token_type, token = authorization_header.split(' ', 1)
                if token_type.lower() == 'bearer':
                    decoded_token = auth.verify_id_token(token)
                    uid = decoded_token.get('uid')
                    
                    try:
                        user = MyUser.objects.get(FirebaseUID=uid)
                    except MyUser.DoesNotExist:
                        print(f'User with FirebaseUID {uid} does not exist.')
                        logger.error(f'User with FirebaseUID {uid} does not exist.')
                        return HttpResponseForbidden('User not found')
                    
                    try:
                        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                        print(f'User {user} logged in successfully')
                    except Exception as e:
                        print(f'Error during login for user {user}: {e}')       
                        logger.error(f'Error during login for user {user}: {e}')
                        return HttpResponseForbidden('Login failed')

                else:
                    print("Authorization header is not of type Bearer")
                    logger.warning('Authorization header is not of type Bearer')
                    return HttpResponseForbidden('Authorization header is not of type Bearer')
            except ValueError:
                logger.error('Error processing the Authorization header')
                return HttpResponseForbidden('Error processing the Authorization header')
            except auth.InvalidIdTokenError:
                print("Invalid ID token")
                #토큰을 프린트해본비ㅏㄷ
                print(token)
                logger.error('Invalid ID token')
                return HttpResponseForbidden('Invalid token')
            except exceptions.FirebaseError as e:
                print(f'Firebase authentication error: {e}')
                logger.error(f'Firebase authentication error: {e}')
                return HttpResponseForbidden('Firebase authentication error')
        else:
            print("No Authorization header provided")
            logger.warning('No Authorization header provided')
            return HttpResponseForbidden('No Authorization header provided')

        return self.get_response(request)