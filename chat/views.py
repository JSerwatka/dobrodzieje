from django.http.response import JsonResponse
from django.urls.base import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import Http404
from django.views.generic.edit import DeleteView

from webapp.models import Team, Creator
from .models import Message
from .serializers import serialize_message

from django.views.generic import (
    ListView,
    View,
    UpdateView,
)

from .forms import TeamForm

# Create your views here.
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
    # members = team.teammember_set.all()
    current_user_admin = members.filter(creator__user=request.user).first().is_admin
    organization = team.announcement.organization
    #TODO settings - delete group, open/close, add looking_for, add stack

    return render(request, 'chat/chatroom.html', {
        'team_id': team_id,
        'team': team,
        'members': members,
        'organization': organization,
        'user_is_admin': current_user_admin,
        'form': TeamForm(instance=team)
    })

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
    success_url = ''

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


#TODO set only for admin authenthication
class RemoveUserFromTeam(View):
    #TODO handle , remove team member view
    def delete(self, request, *args, **kwargs):
        team_id = self.kwargs.get('team_id')
        print(request, args, kwargs)






# class LoadMessages(ListView):
#     model = Message
#     paginate_by = 10

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.page_num = 1

#     # Get the next page of messages
#     def get_context_data(self, **kwargs) :
#         context = super().get_context_data(**kwargs)
#         team_id = self.kwargs.get('team_id')
#         msgs = Message.objects.filter(team_id=team_id)
#         paginator = Paginator(msgs, self.paginate_by)
       
#         try:
#             msg_page = paginator.page(self.page_num)
#             self.page_num += 1
#         except PageNotAnInteger:
#             msg_page = paginator.page(1)
#         except EmptyPage:
#             msg_page = paginator.page(paginator.num_pages)
        
#         print(msg_page)

#         context['object_list'] = msg_page.object_list
#         return context


#     def render_to_response(self, context, **response_kwargs):
#         data = serializers.serialize('json', context['object_list'])
#         print(data)
#         print(context['object_list'])
#         # print(context)
#         return JsonResponse(data, **response_kwargs)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    # print(page_obj)
    # print(page_obj.object_list)
    # return JsonResponse({'test': 'ok'})

