from django.db import models
from django.utils import timezone

class ChatSession(models.Model):
    session_key = models.CharField(max_length=100, unique=True, verbose_name="세션 키")
    question_count = models.IntegerField(default=0, verbose_name="질문 횟수")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일시")

    MAX_QUESTIONS = 10

    class Meta:
        verbose_name = "채팅 세션"
        verbose_name_plural = "채팅 세션"

    def can_ask_question(self):
        return self.question_count < self.MAX_QUESTIONS     

    def increment_count(self):
        self.question_count += 1
        self.save()

    def get_remaining_questions(self):
        return self.MAX_QUESTIONS - self.question_count     

    def __str__(self):
        return f"세션 {self.session_key} ({self.question_count}/{self.MAX_QUESTIONS})"

class ChatConversation(models.Model):
    session = models.ForeignKey(ChatSession,on_delete=models.CASCADE, related_name='conversations')     
    user_question = models.TextField(verbose_name="사용자 질문")
    ai_response = models.TextField(verbose_name="AI 답변")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="대화시간")
    response_time = models.FloatField(null=True, blank=True, verbose_name="응답시간(초)")
    tokens_used = models.IntegerField(null=True, blank=True, verbose_name="사용된 토큰")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="대화시간")

    class Meta:
        verbose_name = "채팅 대화"
        verbose_name_plural = "채팅 대화"
        ordering = ['timestamp']

    def __str__(self):
        return f"Q: {self.user_question[:30]}... | A:{self.ai_response[:30]}..."

    def get_formatted_time(self):
            return self.timestamp.strftime("%y.%m.%d.%H:%M:%S")