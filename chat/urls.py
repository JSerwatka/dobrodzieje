from django.urls import path
from . import views

app_name='chat'
urlpatterns = [
    path('<int:team_id>', views.team_chat, name='team_chat')
]
