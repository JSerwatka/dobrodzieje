from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from webapp.models import (
    Announcement,
    User,
    Team,
    Creator,
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
        organization_user = request.user
        creator_user = User.objects.get(id=request.POST.get('creator'))
        notification_type = Notification.NotificationType.JOIN_REQUEST

        # Check if join request from this user exists
        try:
            Notification.objects.get(sender=creator_user, recipient=organization_user, notification_type=notification_type)
        except Notification.DoesNotExist:
            messages.error(
                request, 
                message='Ten użytkownik nie wysłał prośby.',
                extra_tags='alert-danger'
            )
            return redirect(reverse_lazy('webapp:index'))

        # Create a new Team
        new_team = Team.objects.create_from_organization_user(organization_user=organization_user)
        # new_team = Team.objects.create(
        #     announcement=Announcement.objects.get(organization__user=organization)
        # )
                                                           
        # Add the user as a TeamMember admin 
        # TeamMember.objects.create(
        #     #TODO use related_name to grab creator from user
        #     creator=Creator.objects.get(user=creator_user),
        #     team=new_team,
        #     is_admin=True
        # )

        # Delete all notifications of type JOIN_REQUEST
        # Notification.objects.filter(recipient=organization_user, notification_type=notification_type).delete()
        
        # Create notification that users request got accepted
        # Notification.objects.create(
        #     sender=organization_user, 
        #     recipient=creator_user, 
        #     notification_type=Notification.NotificationType.JOIN_RESPONSE,
        #     #TODO add url to the team chat
        # )
        
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