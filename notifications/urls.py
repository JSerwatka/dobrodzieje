from django.urls import path
from . import views

app_name='notifications'
urlpatterns = [
    path('join-announcement', views.JoinAnnouncement.as_view(), name='join-announcement'),
    path('cancel-join-announcement', views.CancelJoinAnnouncement.as_view(), name='cancel-join-announcement'),
]
