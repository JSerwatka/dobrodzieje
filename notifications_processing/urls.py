from django.urls import path
from . import views

app_name='notifications_processing'
urlpatterns = [
    path('join-announcement', views.join_announcement, name='join-announcement'),
]
