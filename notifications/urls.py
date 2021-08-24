from django.urls import path
from . import views

app_name='notifications'
urlpatterns = [
    path('join-announcement', views.JoinAnnouncement.as_view(), name='join-announcement'),
]
