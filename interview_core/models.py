from django.db import models
from django.contrib.auth.models import User
import json

class InterviewSession(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    topic = models.CharField(max_length=100)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    total_score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.topic} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

class Question(models.Model):
    text = models.TextField()
    topic = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=20, choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], default='medium')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]

class Response(models.Model):
    session = models.ForeignKey(InterviewSession, related_name='responses', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to='responses/')
    transcription = models.TextField(blank=True, null=True)
    ai_feedback = models.JSONField(blank=True, null=True)  # Stores detailed feedback, improvement tips
    score = models.IntegerField(default=0)  # 1-10
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response to {self.question.id} in Session {self.session.id}"
