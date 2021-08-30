from django.http.response import JsonResponse
from django.urls.base import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import Http404
from django.views.generic.edit import DeleteView
from webapp.models import Team, Creator, TeamMember
from .models import Message
from .serializers import serialize_message

from django.views.generic import (
    ListView,
    View,
    UpdateView,
)

from .forms import TeamForm, TeamMemberNickForm

# Create your views here.
#TODO accept only joined team members
def team_chat(request, team_id):
    # Check if the team exists and the current user is authorized to view its chat
    #TODO make sure it works for unauthenticated users
    #TODO change to  auhtontication test method
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
    
    members = team.teammember_set.select_related('creator__user')
    current_member = members.get(creator__user=request.user)

    # New members have to enter their nick
    if not current_member.joined:
        return redirect(
                reverse_lazy('chat:choose-nick', 
                kwargs={
                    'team_id': team_id,
                    'team_member_id': current_member.id
                }))

    current_member_admin = current_member.is_admin
    organization = team.announcement.organization

    return render(request, 'chat/chatroom.html', {
        'team_id': team_id,
        'team': team,
        'members': members,
        'organization': organization,
        'user_is_admin': current_member_admin,
        'form': TeamForm(instance=team)
    })


#TODO add auhtontication test method + restrict to joined users
class ChooseNick(UpdateView):
    form_class = TeamMemberNickForm
    template_name = 'chat/choose_nick.html'

    def get_object(self):
        team_member_id = self.kwargs.get('team_member_id')
        return TeamMember.objects.get(id=team_member_id)

    def form_valid(self, form):
        # team member joined the team
        form.instance.joined = True
        form.instance.save()
        return super().form_valid(form)

    def get_success_url(self):
        team_id = self.kwargs.get('team_id')
        return reverse_lazy('chat:team-chat', kwargs={'team_id': team_id})


#TODO add auhtontication test method
class LoadMessages(ListView):
    paginate_by = 25
    
    def get_queryset(self):
        team_id = self.kwargs.get('team_id')
        return Message.objects.filter(team_id=team_id)

    # Serialize current's page msgs and send as json
    def render_to_response(self, context, **response_kwargs):
        msgs_page = context['page_obj'].object_list
        data = [serialize_message(msg_obj) for msg_obj in msgs_page]
        num_pages = context['paginator'].num_pages

        response = {
            'data': data,
            'numPages': num_pages
        } 
        return JsonResponse(response, **response_kwargs)


#TODO set only for admin authenthication + admin
class UpdateTeamSettings(UpdateView):
    model = Team
    form_class = TeamForm
    http_method_names = ['post']

    #TODO handle open/close, add looking_for, add stack views
    def get_object(self):
        team_id = self.kwargs.get('team_id')
        return Team.objects.get(id=team_id)

    def get_success_url(self):
        team_id = self.kwargs.get('team_id')
        return reverse_lazy('chat:team-chat', kwargs={'team_id': team_id})


#TODO set only for admin authenthication + admin
class DeleteTeam(DeleteView):
    def get_object(self):
        team_id = self.kwargs.get('team_id')
        return Team.objects.get(id=team_id)

    def get_success_url(self):
        return reverse_lazy('webapp:index')


#TODO set only for admin authenthication + admin
class RemoveUserFromTeam(DeleteView):
    def get_object(self):
        member_id = self.request.POST.get('member-id')
        return TeamMember.objects.get(id=member_id)
    def get_success_url(self):
        team_id = self.kwargs.get('team_id')
        return reverse_lazy('chat:team-chat', kwargs={'team_id': team_id})
