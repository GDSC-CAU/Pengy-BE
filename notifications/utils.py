# notifications/utils.py
from firebase_admin import credentials, messaging
from users.models import Device

import google.generativeai as genai
from config.settings import get_env_variable


def send_to_firebase_cloud_messaging(token, title, body, deep_link=None):
    """FCM을 통해 알림 메시지를 전송하는 함수"""

    print("send_to_firebase_cloud_messaging 함수가 실행됐습니다.")
    print("title:", title)
    print("body:", body)
    print("deep_link:", deep_link)
    
    # deep_link가 None이거나 문자열이 아닌 경우를 처리
    deep_link_str = "" if deep_link is None else str(deep_link)
    
    # 메시지 객체 생성
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
        data={
            "url": deep_link_str,  # 변환된 문자열 사용
        },
    )
    
    # 메시지 전송 시도
    try:
        response = messaging.send(message)
        print(f"Successfully sent message: {response}")
    except Exception as e:
        print(f'except {message}')
        print(f"Failed to send message: {e}")


def get_user_device_tokens(user):
    """특정 사용자의 모든 디바이스 토큰을 리스트로 반환"""
    devices = Device.objects.filter(user=user)
    return [device.fcmToken for device in devices if device.fcmToken]


# API 키 설정
api_key = get_env_variable('GEMINI_API_KEY') # 보안!!!!!
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')
def generate_message_content():
    """gemini-pro를 사용해서 오늘의 화재 예방 tip을 반환하는 함수"""
    prompt = """
        Act as a fire prevention expert. 
        Most fires are caused by carelessness. To prevent carelessness, we're sending out a Fire Prevention Tip of the Day to prevent fires.
        The fire prevention tip of the day should be accurate and practical for people.
        Write a specific and professional fire prevention tip in just one sentence.
        please be as much professional as possible.
        Here's a sample sentence 
        "An arc-fault circuit interrupter (AFCI) shuts off electricity when a dangerous situation arises. Consider installing one in your home."
    """
    try:
        response = model.generate_content(prompt)
        # 여기서는 response 객체가 text 속성을 가진다고 가정합니다.
        # 실제 사용하는 라이브러리의 응답 구조에 따라 접근 방식을 조정해야 합니다.
        body = response.text.strip()
    except Exception as e:
        # 예외 처리: 로그 기록, 기본 메시지 반환 등을 여기서 수행
        print(f"Error generating fire prevention tip: {e}")
        body = "An arc-fault circuit interrupter (AFCI) shuts off electricity when a dangerous situation arises. Consider installing one in your home."
    print(body)
    return body

