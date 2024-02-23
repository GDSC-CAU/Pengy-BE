# config/tests.py

from django.test import TestCase, Client
from django.urls import reverse

# 미들웨어가 작동하는지 테스트
class MiddlewareTest(TestCase):
    def test_firebase_middleware(self):
        client = Client()
        
        # 인증 헤더 없이 요청 보내기
        response = client.get(reverse('eduContents:api-root'))
        self.assertEqual(response.status_code, 200)  # 또는 기대하는 상태 코드
        
        # 유효한/유효하지 않은 토큰으로 테스트
        response = client.get(reverse('eduContents:api-root'), HTTP_AUTHORIZATION='Bearer your_token_here')
        self.assertEqual(response.status_code, 200)  # 또는 기대하는 상태 코드
