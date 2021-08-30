from django.urls import path
from . import views

app_name='notifications'
urlpatterns = [
    #Join announcement
    path('join-announcement', views.JoinAnnouncement.as_view(), name='join-announcement'),
    path('cancel-join-announcement', views.CancelJoinAnnouncement.as_view(), name='cancel-join-announcement'),
    path('join-announcement-acceptance', views.JoinAnnouncementAcceptance.as_view(), name='join-announcement-acceptance'),
    path('join-announcement-rejection', views.JoinAnnouncementRejection.as_view(), name='join-announcement-rejection'),
    # Join Team
    path('join-team', views.JoinTeam.as_view(), name='join-team'),
    path('cancel-join-team', views.CancelJoinTeam.as_view(), name='cancel-join-team'),
    path('join-team-acceptance', views.JoinTeamAcceptance.as_view(), name='join-team-acceptance'),
    path('join-team-rejection', views.JoinTeamRejection.as_view(), name='join-team-rejection'),
]
