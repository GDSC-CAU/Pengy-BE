from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .utils import generate_quiz
from .models import Quiz, UserScore
import random
import re
from firebase_admin import auth, exceptions
from django.contrib.auth import login
from users.models import MyUser
from rest_framework import status

class GetUserScoreView(APIView):
    """Get the user's fish score."""
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_score, created = UserScore.objects.get_or_create(user=request.user)
        return Response({
            "status": "success",
            "fish_score": user_score.fish_score
        })


class GetQuizzesView(APIView):
    permission_classes = [IsAuthenticated]
    """Get a set of 5 random quizzes."""

    def get(self, request, *args, **kwargs):
        quizzes_count = Quiz.objects.count()
        if quizzes_count < 5:
            return Response({
                "status": "error",
                "message": "Not enough quizzes available."
            }, status=400)

        random_ids = random.sample(list(Quiz.objects.values_list('id', flat=True)), 5)
        quizzes = Quiz.objects.filter(id__in=random_ids)
        
        quizzes_data = [{"question": quiz.question, "answer": quiz.answer} for quiz in quizzes]

        return Response({
            "status": "success",
            "quizzes": quizzes_data
        })
    
class GenerateQuizView(APIView):
    """ Generate quizzes from the quiz content and save them to the database."""

    def post(self, request, *args, **kwargs):
        try:
            print("Generating quizzes...")
            # Assuming generate_quiz() is defined elsewhere and returns the quiz content
            quiz_content = generate_quiz()
            print("Generating finished!")
            quizzes = self.parse_quiz_content(quiz_content)

            for question, answer_bool, explanation in quizzes:
                Quiz.objects.create(question=question, answer=answer_bool, explanation=explanation)

            return Response({"status": "success", "message": "Quizzes generated and saved successfully."})
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=400)

    def parse_quiz_content(self, quiz_content):
        quizzes = []

        # 업데이트된 정규식 패턴을 사용하여 질문, 답변 지시자(O/X), 설명을 추출합니다.
        pattern = r"\(([^;]+?);\s*(O|X);\s*(.*?)\)"
        matches = re.findall(pattern, quiz_content, re.DOTALL)

        for match in matches:
            question, answer, explanation = match
            answer_bool = True if answer == 'O' else False
            quizzes.append((question.strip(), answer_bool, explanation.strip()))

        return quizzes
    

class UpdateUserScoreView(APIView):
    """ Update the user's fish score."""

    def post(self, request, *args, **kwargs):
        try:
            authorization_header = request.headers.get('Authorization')
            if authorization_header and authorization_header.startswith('Bearer '):
                id_token = authorization_header.split(' ')[1]
            else:
                print("Authorization header is missing or invalid")
                return Response({'error': 'Authorization header is missing or invalid'}, status=status.HTTP_401_UNAUTHORIZED)

            try: 
                decoded_token = auth.verify_id_token(id_token)
                uid = decoded_token['uid']  
                user = MyUser.objects.get(FirebaseUID=uid)

                # Perform Django login
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                data = request.data
                additional_score = data.get('correct_answers_count', 0)

                user_score, _ = UserScore.objects.get_or_create(user=user)
                user_score.fish_score += additional_score
                user_score.save()
            
            except exceptions.FirebaseError as ex:
                error_message = f'Firebase error: {ex.message}' if hasattr(ex, 'message') else 'Firebase authentication error'
                print(error_message)
                return Response({'error': error_message}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({
                "status": "success",
                "message": "User score updated successfully.",
                "new_fish_score": user_score.fish_score
            })
        except Exception as e:
            return Response({
                "status": "error",
                "message": f"Error updating user score: {str(e)}"
            }, status=400)