from django.urls import path
from .views import GetUserScoreView, GenerateQuizView, GetQuizzesView, UpdateUserScoreView

app_name = 'quizzes'

urlpatterns = [
    path('get-score/', GetUserScoreView.as_view(), name='user_score'),
    path('generate-quiz/', GenerateQuizView.as_view(), name='generate_quiz'),
    path('get-quiz/', GetQuizzesView.as_view(), name='get_quizzes'),
    path('update-score/', UpdateUserScoreView.as_view(), name='update_score'),
]
