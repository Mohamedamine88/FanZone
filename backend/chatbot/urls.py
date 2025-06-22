from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('message/', views.ChatbotView.as_view(), name='message'),
] 