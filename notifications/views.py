from django.shortcuts import render, redirect
from webapp.models import (
    User
)

from .models import Notification
from django.views.generic import View

# Create your views here.
def join_announcement(request):
    #TODO add try except for icorrect data send by user
    if request.method == 'POST':
        sender = request.user
        recipient = User.objects.get(id=request.POST.get('organization'))
        notification_type = Notification.NotificationType.JOIN_REQUEST
        message = 'chce pracować nad Twoją nową stroną'
        Notification.objects.create(
            sender = sender,
            recipient = recipient,
            message = message,
            notification_type = notification_type
        )
        return redirect(request.META.get('HTTP_REFERER'))

# def cancel_join_announcement(request):
#     if request.method == 'POST':
#         print(dir(request))