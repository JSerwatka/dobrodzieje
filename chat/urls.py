from django.urls import path
from . import views

app_name='chat'
urlpatterns = [
    path('<int:team_id>', views.team_chat, name='team-chat'),
    path('<int:team_id>/wiadomosci', views.LoadMessages.as_view(), name='load-messages'),
    path('<int:team_id>/ustawienia', views.UpdateTeamSettings.as_view(), name='update-team-settings'),
    path('<int:team_id>/czlonkowie', views.RemoveUserFromTeam.as_view(), name='delete-team-members'),
]
