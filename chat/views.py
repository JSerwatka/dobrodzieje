from django.urls.base import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import Http404

from webapp.models import Team, Creator

# Create your views here.
def team_chat(request, team_id):
    # Check if the team exists and the current user is authorized to view its chat
    try:
        Team.objects.get(id=team_id).members.get(user=request.user)
    except Team.DoesNotExist as e:
        raise Http404('Drużyna nie istnieje')
    except Creator.DoesNotExist:
        messages.error(
            request, 
            message='Nie masz uprawnień do tego czatu. Aby z niego skorzystać, poproś o dołączenie.',
            extra_tags='alert-danger'
        )
        return redirect(reverse_lazy('webapp:index'))
        # raise

    return render(request, 'chat/chatroom.html', {
        'team_id': team_id
    })