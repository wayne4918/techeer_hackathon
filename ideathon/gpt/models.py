from django.db import models

class Character(models.Model):
    character_name = models.CharField(max_length=100)
    tone = models.CharField(max_length=100)
    text_length = models.CharField(max_length=10)  # 길게, 짧게와 같은 선택지를 저장
    situation = models.CharField(max_length=255)  # 상황 설명을 저장
    language = models.CharField(max_length=100)

class GptAnswer(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)  # Character 모델과 연결
    response_content = models.TextField()  # GPT가 생성한 응답 내용