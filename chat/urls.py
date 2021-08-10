from django.urls import path
from . import views

app_name='chat'
urlpatterns = [
    path('<int:team_id>', views.team_chat, name='team-chat'),
    path('<int:team_id>/wiadomosci', views.LoadMessages.as_view(), name='load-messages'),
    path('<int:team_id>/status', views.UpdateGroupStatus.as_view(), name='update-status'),
    path('<int:team_id>/czlonkowie', views.RemoveUserFromGroup.as_view(), name='delete-team-members'),
    path('<int:team_id>/stack', views.UpdateGroupStack.as_view(), name='update-stack'),
    path('<int:team_id>/poszukiwani', views.UpdateGroupLookingFor.as_view(), name='update-looking-for'),
]
