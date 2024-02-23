from django.contrib import admin
from .models import UserScore, Quiz

@admin.register(UserScore)
class UserScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'fish_score')
    search_fields = ('user__email', 'fish_score')
    list_filter = ('user', 'fish_score')

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')
    search_fields = ('question',)
    list_filter = ('answer',)
