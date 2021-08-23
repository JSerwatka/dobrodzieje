from django.shortcuts import render, redirect
from webapp.models import (
    User
)

# Create your views here.
def join_announcement(request):
    #TODO add try except for icorrect data send by user
    if request.method == 'POST':
        actor = User.objects.get(id=request.user.id)
        recipient = User.objects.get(id=request.POST.get('organization'))
        notification_type = 'Join Announcement'
        message = 'chce pracować nad Twoją nową stroną'
        # notify.send(actor, recipient=recipient, verb=notification_type, description=message)
        return redirect(request.META.get('HTTP_REFERER'))

# def cancel_join_announcement(request):
#     if request.method == 'POST':
#         print(dir(request))