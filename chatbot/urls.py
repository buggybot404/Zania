# myapi/urls.py
from django.urls import path
from .views import generate_chatbot_answers

urlpatterns = [
    path('v1/get_answers', generate_chatbot_answers, name='generate_chatbot_response'),
]
