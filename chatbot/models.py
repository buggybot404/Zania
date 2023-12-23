# models.py
from django.db import models


class ChatbotResponse(models.Model):
    message = models.CharField(max_length=255)
    response_code = models.IntegerField()
    response = models.JSONField()

    def __str__(self):
        return self.message
