from django.shortcuts import render, redirect
from webapp.models import (
    User
)

from .models import Notification
from django.views.generic import View

# Create your views here.
class JoinAnnouncement(View):
    #TODO add try except for icorrect data send by user
    def post(self, request, *args, **kwargs):
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

class CancelJoinAnnouncement(View):
    #TODO add try except for icorrect data send by user
    def post(self, request, *args, **kwargs):
        sender = request.user
        recipient = User.objects.get(id=request.POST.get('organization'))
        notification_type = Notification.NotificationType.JOIN_REQUEST
        Notification.objects.filter(sender=sender, recipient=recipient, notification_type=notification_type).delete()
        return redirect(request.META.get('HTTP_REFERER'))