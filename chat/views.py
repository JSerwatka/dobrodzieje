from django.urls.base import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import Http404

from webapp.models import Announcement, Team, Creator

# Create your views here.
def team_chat(request, team_id):
    # Check if the team exists and the current user is authorized to view its chat
    try:
        team = Team.objects.get(id=team_id)
        team.members.get(user=request.user)
    except Team.DoesNotExist:
        raise Http404('Drużyna nie istnieje')
    except Creator.DoesNotExist:
        messages.error(
            request, 
            message='Nie masz uprawnień do tego czatu. Aby z niego skorzystać, poproś o dołączenie.',
            extra_tags='alert-danger'
        )
        return redirect(reverse_lazy('webapp:index'))
    
    members = team.teammember_set.all()
    organization = team.announcement.organization
    #TODO settings - delete group, open/close, add looking_for, add stack

    return render(request, 'chat/chatroom.html', {
        'team_id': team_id,
        'team': team,
        'members': members,
        'organization': organization
    })