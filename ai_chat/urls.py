from django.urls import path
from . import views

app_name = 'ai_chat'
urlpatterns = [
    path('send/', views.send_message,
name='send_message'),
    path('history/', views.get_chat_history,
name='chat_history'),
]