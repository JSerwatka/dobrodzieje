from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from webapp.models import (
    Announcement,
    User,
    Team,
    TeamMember
)

from .models import Notification
from django.views.generic import View

# Create your views here.
class JoinAnnouncement(View):
    #TODO add try except for icorrect data send by user
    #TODO use superclass to make it DRY
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
    #TODO use superclass to make it DRY
    def post(self, request, *args, **kwargs):
        sender = request.user
        recipient = User.objects.get(id=request.POST.get('organization'))
        notification_type = Notification.NotificationType.JOIN_REQUEST
        Notification.objects.get(sender=sender, recipient=recipient, notification_type=notification_type).delete()
        return redirect(request.META.get('HTTP_REFERER'))


class JoinAnnouncementAcceptance(View):
    #TODO add try except for icorrect data send by user
    #TODO use superclass to make it DRY
    def post(self, request, *args, **kwargs):
        # Get data from the form
        organization = request.user
        creator = User.objects.get(id=request.POST.get('creator'))
        notification_type = Notification.NotificationType.JOIN_REQUEST

        # Check if join request from this user exists
        try:
            Notification.objects.get(sender=creator, recipient=organization, notification_type=notification_type)
        except Notification.DoesNotExist:
            messages.error(
                request, 
                message='Ten użytkownik nie wysłał prośby.',
                extra_tags='alert-danger'
            )
            return redirect(reverse_lazy('webapp:index'))

        # Create a new Team
        Team.objects.create(
            announcement=Announcement.objects.get(organization__user=organization)
        )
                                                           
        
        # Add the user as TeamMember admin 
        # #TODO Do it when a creator first enters team
        # #TODO create joined field in TeamMember model to check if he should go through setup??
        # TeamMember.objects.create(
        #     creator__user=creator,
        #     team=new_team

        # )

        # Delete all notifications of type JOIN_REQUEST
        Notification.objects.filter(recipient=organization, notification_type=notification_type).delete()
        
        # Create notification that users request got accepted
        Notification.objects.create(
            sender=organization, 
            recipient=creator, 
            notification_type=Notification.NotificationType.JOIN_RESPONSE,
            #TODO add url to the team chat
        )
        
        # Redirect to the announcement
        return redirect(request.META.get('HTTP_REFERER'))  #TODO change to announcement   


class JoinAnnouncementRejection(View):
    #TODO add try except for icorrect data send by user
    #TODO use superclass to make it DRY
    def post(self, request, *args, **kwargs):
        sender = request.user
        recipient = User.objects.get(id=request.POST.get('organization'))
        notification_type = Notification.NotificationType.JOIN_REQUEST
        return redirect(request.META.get('HTTP_REFERER'))