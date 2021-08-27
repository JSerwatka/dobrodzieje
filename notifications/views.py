from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from webapp.models import (
    Announcement,
    Organization,
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
        notification_type = Notification.NotificationType.JOIN_ANNOUNCEMENT_REQUEST
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
        notification_type = Notification.NotificationType.JOIN_ANNOUNCEMENT_REQUEST
        Notification.objects.get(sender=sender, recipient=recipient, notification_type=notification_type).delete()
        return redirect(request.META.get('HTTP_REFERER'))


class JoinAnnouncementAcceptance(View):
    #TODO add try except for icorrect data send by user
    #TODO use superclass to make it DRY
    def post(self, request, *args, **kwargs):
        # Get data from the form
        organization_user = request.user
        creator_user = User.objects.get(id=request.POST.get('creator'))
        notification_type = Notification.NotificationType.JOIN_ANNOUNCEMENT_REQUEST

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
        organization_announcement = Announcement.objects.get(organization__user=organization_user)
        new_team = Team.objects.create(
            announcement = organization_announcement
        )
                                                           
        # Add the user as a TeamMember admin 
        TeamMember.objects.create(
            creator = creator_user.creator,
            team = new_team,
            is_admin = True
        )

        # Notify all rejected users
        all_join_requests = Notification.objects.filter(recipient=organization_user, notification_type=notification_type)
        join_requests_rejected = all_join_requests.exclude(sender=creator_user)
        for join_request in join_requests_rejected:
            Notification.objects.create(
                sender = organization_user, 
                recipient = join_request.sender, 
                notification_type = Notification.NotificationType.JOIN_RESPONSE,
                message = 'Argh! Inne zgłoszenie zostało już przyjęte do tego ogłoszenia. Spróbuje gdzie indziej i nie trać zapału!'
            )

        # Delete all join request notifications
        all_join_requests.delete()
        
        # Create notification that the user's request got accepted
        Notification.objects.create(
            sender = organization_user, 
            recipient = creator_user, 
            notification_type = Notification.NotificationType.JOIN_RESPONSE,
            message = f'Gratulacje twoja prośba o dołączenie do {organization_user.organization} została zaakcaptowana!',
            related_url = new_team.get_absolute_url()
        )

        # Add message that the user is working on your website
        messages.info(
            request, 
            message='Gratulacje! Twoja strona już się tworzy!',
            extra_tags='alert-success'
        )
        
        # Redirect to the announcement
        return redirect(organization_announcement.get_absolute_url())


class JoinAnnouncementRejection(View):
    #TODO add try except for icorrect data send by user
    #TODO use superclass to make it DRY
    def post(self, request, *args, **kwargs):
        # Get data from the form
        organization_user = request.user
        creator_user = User.objects.get(id=request.POST.get('creator'))
        notification_type = Notification.NotificationType.JOIN_ANNOUNCEMENT_REQUEST

        # Check if join request from this user exists
        try:
            join_request_notif = Notification.objects.get(sender=creator_user, recipient=organization_user, notification_type=notification_type)
        except Notification.DoesNotExist:
            messages.error(
                request, 
                message='Ten użytkownik nie wysłał prośby.',
                extra_tags='alert-danger'
            )
            return redirect(reverse_lazy('webapp:index'))

        # Create notification that the user's request got rejected
        Notification.objects.create(
            sender = organization_user, 
            recipient = creator_user, 
            notification_type = Notification.NotificationType.JOIN_RESPONSE,
            message = f'😢 Twoja prośba o dołączenie do {organization_user.organization} została odrzucona. Skontaktuj się z organizacją jeśli chcesz wyjaśnić sytuację',
        )

        # Delete this join request notification
        join_request_notif.delete()

        return redirect(request.META.get('HTTP_REFERER'))

class JoinTeam(View):
    #TODO add try except for icorrect data send by user
    #TODO use superclass to make it DRY
    def post(self, request, *args, **kwargs):
        form_data = request.POST
        
        # Confirm that the team is opened and is looking for this role
        team = get_object_or_404(
                    Team,
                    id = form_data['team_id'],
                    is_closed = False,
                    looking_for__contains = [form_data['looking_for']]
                )

        organization = get_object_or_404(Organization, user__id=form_data['organization'])

        # Gather all the data and send notification to the team's admin
        sender = request.user
        recipient = team.get_admin()
        notification_type = Notification.NotificationType.JOIN_TEAM_REQUEST
        message = f'chce dołączyć do drużyny dla {organization}'
        extra_data = {'team_id': team.id}
        Notification.objects.create(
            sender = sender,
            recipient = recipient,
            message = message,
            notification_type = notification_type,
            extra_data = extra_data
        )
        return redirect(request.META.get('HTTP_REFERER'))


class CancelJoinTeam(View):
    #TODO add try except for icorrect data send by user
    #TODO use superclass to make it DRY
    def post(self, request, *args, **kwargs):
        sender = request.user
        recipient = User.objects.get(id=request.POST.get('team-admin'))
        notification_type = Notification.NotificationType.JOIN_TEAM_REQUEST
        Notification.objects.get(sender=sender, recipient=recipient, notification_type=notification_type).delete()
        return redirect(request.META.get('HTTP_REFERER'))