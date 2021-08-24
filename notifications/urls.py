from django.urls import path
from . import views

app_name='notifications'
urlpatterns = [
    path('join-announcement', views.JoinAnnouncement.as_view(), name='join-announcement'),
    path('cancel-join-announcement', views.CancelJoinAnnouncement.as_view(), name='cancel-join-announcement'),
    path('join-announcement-rejection', views.JoinAnnouncementRejection.as_view(), name='join-announcement-rejection'),
    path('join-announcement-acceptance', views.JoinAnnouncementAcceptance.as_view(), name='join-announcement-acceptance'),
]
