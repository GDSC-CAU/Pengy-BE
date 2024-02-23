from django.db import models
from users.models import MyUser  

class UserScore(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, verbose_name="유저")
    #fish_score default는 0으로 설정
    fish_score = models.IntegerField(default=0, verbose_name="Fish Score")

    def __str__(self):
        return f"{self.user.email} - Fish Score: {self.fish_score}"

class Quiz(models.Model):
    question = models.CharField(max_length=255, verbose_name="문제")
    answer = models.BooleanField(verbose_name="정답")
    explanation = models.TextField(verbose_name="문제해설")

    def __str__(self):
        return self.question

