from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.html import format_html
from webapp.models import (
    Announcement,
    Organization,
    User,
    Team,
    Creator,
    TeamMember,
    Roles
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
            announcement = organization_announcement,
            is_closed = True
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
                message='Ten użytkownik nie wysłał prośby',
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
        role_value = form_data['looking_for']
        
        # Confirm that the team is opened and is looking for this role
        team = get_object_or_404(
                    Team,
                    id = form_data['team_id'],
                    is_closed = False,
                    looking_for__contains = [role_value]
                )

        #TODO handle with correct reponse status
        # Get data for the notification's message
        organization = get_object_or_404(Organization, user__id=form_data['organization'])
        role_name = Roles.get_labels_by_values(role_value)[0]

        # Gather all the data and send notification to the team's admin
        sender = request.user
        recipient = team.get_admin()
        notification_type = Notification.NotificationType.JOIN_TEAM_REQUEST
        message = f'chce dołączyć do drużyny dla {organization} na stanowisko {role_name}'
        extra_data = {'team_id': team.id, 
                      'role': {'value': role_value, 'name': role_name},
                      'organization': organization.name
                    }
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
        #TODO handle with correct reponse status
        team = get_object_or_404(Team, id=request.POST['team_id'], is_closed=False)

        sender = request.user
        recipient = team.get_admin()
        notification_type = Notification.NotificationType.JOIN_TEAM_REQUEST

        Notification.objects.get(
            sender=sender, 
            recipient=recipient, 
            notification_type=notification_type, 
            extra_data__team_id = team.id
        ).delete()

        return redirect(request.META.get('HTTP_REFERER'))


class JoinTeamAcceptance(View):
    #TODO add try except for icorrect data send by user
    #TODO use superclass to make it DRY
    def post(self, request, *args, **kwargs):
        # Get data from the form
        team_admin = request.user
        applicant = User.objects.get(id=request.POST.get('creator'))
        team = Team.objects.get(id=request.POST.get('team-id'))
        notification_type = Notification.NotificationType.JOIN_TEAM_REQUEST
        
        # Check if join request from this user exists
        try:
            join_request_notif = Notification.objects.get(
                sender = applicant, 
                recipient = team_admin, 
                notification_type = notification_type,
                extra_data__team_id = team.id
            )
        except Notification.DoesNotExist:
            messages.error(
                request, 
                message='Ten użytkownik nie wysłał prośby o dołączenie do tej drużyny',
                extra_tags='alert-danger'
            )
            return redirect(reverse_lazy('webapp:index'))

        # Get the role the applicant in applying for and the team's organization name
        role = join_request_notif.extra_data['role']
        organization_name = join_request_notif.extra_data['organization']

        # Add the applicant as a TeamMember
        TeamMember.objects.create(
            creator = applicant.creator,
            team = team,
            role = role['value']
        )

        # Notify the applicant that his/her request got accepted
        Notification.objects.create(
            sender = team_admin, 
            recipient = applicant, 
            notification_type = Notification.NotificationType.JOIN_RESPONSE,
            message = f'Gratulacje twoja prośba o dołączenie do drużyny dla {organization_name} została zaakcaptowana!',
            related_url = team.get_absolute_url()
        )

        # Delete the old notification
        join_request_notif.delete()

        # Add message that the aplicant joined your team
        messages.info(
            request, 
            message=format_html(f'Powitaj nowego członka drużyny na <a href="{team.get_absolute_url()}">czacie gdy dołączy 👋'),
            extra_tags='alert-success'
        )

        return redirect(request.META.get('HTTP_REFERER'))



class JoinTeamRejection(View):
    #TODO add try except for icorrect data send by user
    #TODO use superclass to make it DRY
    def post(self, request, *args, **kwargs):
        # Get data from the form
        team_admin = request.user
        applicant = User.objects.get(id=request.POST.get('creator'))
        notification_type = Notification.NotificationType.JOIN_TEAM_REQUEST

        # Check if join request from this user exists
        try:
            join_request_notif = Notification.objects.get(
                    sender = applicant, 
                    recipient = team_admin, 
                    notification_type = notification_type,
                    extra_data__team_id = int(request.POST.get('team-id'))
            )
        except Notification.DoesNotExist:
            messages.error(
                request, 
                message='Ten użytkownik nie wysłał prośby o dołączenie do tej drużyny',
                extra_tags='alert-danger'
            )
            return redirect(reverse_lazy('webapp:index'))

        # Get the the team's organization name
        organization_name = join_request_notif.extra_data['organization']

        # Create notification that the user's request got rejected
        Notification.objects.create(
            sender = team_admin, 
            recipient = applicant, 
            notification_type = Notification.NotificationType.JOIN_RESPONSE,
            message = f'😢 Twoja prośba o dołączenie do drużyny dla {organization_name} została odrzucona. Powodów może być wiele, więc nie zniechęcaj się',
        )

        # Delete the old notification
        join_request_notif.delete()

        return redirect(request.META.get('HTTP_REFERER'))