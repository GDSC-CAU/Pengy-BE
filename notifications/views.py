from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import MyUser
from .utils import send_to_firebase_cloud_messaging, get_user_device_tokens, generate_message_content

@api_view(['POST'])  # POST 요청만 허용
def send_periodic_notifications_api(request):
    """API를 통해 주기적으로 알림을 전송하는 뷰"""
    users = MyUser.objects.all()
    print("알림 전송이 시작됐습니다.")
    
    title = "🔥 Fire Prevention Tip of the Day 🔥"
    body = generate_message_content()  # 메시지 내용을 동적으로 생성
    deep_link = None

    for user in users:
        device_tokens = get_user_device_tokens(user)
        for token in device_tokens:
            send_to_firebase_cloud_messaging(
                token,
                title,
                body,
                deep_link
            )
    print("알림 전송이 완료됐습니다.")
    return Response({"message": "Notifications sent successfully."})
