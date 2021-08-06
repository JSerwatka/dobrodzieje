from django.shortcuts import render

# Create your views here.
def team_chat(request, team_id):
    return render(request, 'chat/chatroom.html', {
        'team_id': team_id
    })