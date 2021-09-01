from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.html import format_html
from django.views.generic import View

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
from .views_mixins import (
    JoinAnnouncementMixin, 
    JoinAnnouncementResponseMixin,
    JoinTeamResponseMixin
)


class JoinAnnouncement(JoinAnnouncementMixin, View):
    def post(self, request, *args, **kwargs):
        notification_data = super().get_notification_data(request)

        # Handle errors
        if notification_data.get('error_with_redirect'):
            return notification_data['error_with_redirect']
        
        sender = notification_data['sender']
        recipient = notification_data['recipient']
        notification_type = notification_data['notification_type']
        message = f'Użytkownik {sender} chce pracować nad Twoją nową stroną'

        Notification.objects.create(
            sender = sender,
            recipient = recipient,
            message = message,
            notification_type = notification_type
        )
        return redirect(request.META.get('HTTP_REFERER'))


class CancelJoinAnnouncement(JoinAnnouncementMixin, View):
    def post(self, request, *args, **kwargs):
        notification_data = super().get_notification_data(request)

        # Handle errors
        if notification_data.get('error_with_redirect'):
            return notification_data['error_with_redirect']

        sender = notification_data['sender']
        recipient = notification_data['recipient']
        notification_type = notification_data['notification_type']
        try:
            Notification.objects.get(sender=sender, recipient=recipient, notification_type=notification_type).delete()
        except Notification.DoesNotExist:
            messages.error(
                    request, 
                    message='Prośba o stworzenie drużyny nie istnieje  🤷‍♂️',
                    extra_tags='alert-danger'
                )
            return {'error_with_redirect': redirect(reverse_lazy('webapp:index'))}
        return redirect(request.META.get('HTTP_REFERER'))


class JoinAnnouncementAcceptance(JoinAnnouncementResponseMixin, View):
    def post(self, request, *args, **kwargs):
        notification_data = super().get_notification_data(request)

        # Handle errors
        if notification_data.get('error_with_redirect'):
            return notification_data['error_with_redirect']
        
        # Get data from the form
        organization_user = notification_data['organization_user']
        creator_user = notification_data['creator_user']
        notification_type = notification_data['notification_type']

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
        all_join_requests = Notification.objects.filter(recipient=organization_user, 
                                                        notification_type=Notification.NotificationType.JOIN_ANNOUNCEMENT_REQUEST)
        join_requests_rejected = all_join_requests.exclude(sender=creator_user)
        for join_request in join_requests_rejected:
            Notification.objects.create(
                sender = organization_user, 
                recipient = join_request.sender, 
                notification_type = notification_type,
                message = 'Argh! Inne zgłoszenie zostało już przyjęte do tego ogłoszenia. Spróbuje gdzie indziej i nie trać zapału!'
            )

        # Delete all join request notifications
        all_join_requests.delete()
        
        # Create notification that the user's request got accepted
        Notification.objects.create(
            sender = organization_user, 
            recipient = creator_user, 
            notification_type = notification_type,
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


class JoinAnnouncementRejection(JoinAnnouncementResponseMixin, View):
    def post(self, request, *args, **kwargs):
        notification_data = super().get_notification_data(request)

        # Handle errors
        if notification_data.get('error_with_redirect'):
            return notification_data['error_with_redirect']

        organization_user = notification_data['organization_user']
        creator_user = notification_data['creator_user']
        notification_type = notification_data['notification_type']
        join_request_notif = notification_data['join_request_notif']
        message = f'😢 Twoja prośba o dołączenie do {organization_user.organization} została odrzucona. Skontaktuj się z organizacją jeśli chcesz wyjaśnić sytuację'

        # Create notification that the user's request got rejected
        Notification.objects.create(
            sender = organization_user, 
            recipient = creator_user, 
            notification_type = notification_type,
            message = message,
        )

        # Delete this join request notification
        join_request_notif.delete()

        return redirect(request.META.get('HTTP_REFERER'))

class JoinTeam(View):
    def post(self, request, *args, **kwargs):
        form_data = request.POST
        role_value = form_data['looking_for']
        
        try:
            # Confirm that the team is opened and is looking for this role
            team = Team.objects.get(
                        id = form_data['team_id'],
                        is_closed = False,
                        looking_for__contains = [role_value]
                   )
            
            # Get data for the notification's message
            organization = Organization.objects.get(user__id=form_data['organization'])
            role_name = Roles.get_labels_by_values(role_value)[0]
        except Team.DoesNotExist:
            messages.error(
                request, 
                message='Drużyna nie istnieje 🤷‍♂️',
                extra_tags='alert-danger'
            )
            return redirect(reverse_lazy('webapp:index'))
        except Organization.DoesNotExist:
            messages.error(
                request, 
                message='Organizacja nie istnieje 🤷‍♂️',
                extra_tags='alert-danger'
            )
            return redirect(reverse_lazy('webapp:index'))  
        
        
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
    def post(self, request, *args, **kwargs):       
        try:
            team = Team.objects.get(id=request.POST['team_id'], is_closed=False)
        except Team.DoesNotExist:
            messages.error(
                request, 
                message='Drużyna nie istnieje 🤷‍♂️',
                extra_tags='alert-danger'
            )
            return redirect(reverse_lazy('webapp:index'))

        sender = request.user
        recipient = team.get_admin()
        notification_type = Notification.NotificationType.JOIN_TEAM_REQUEST

        try:
            Notification.objects.get(
                sender=sender, 
                recipient=recipient, 
                notification_type=notification_type, 
                extra_data__team_id = team.id
            ).delete()
        except Notification.DoesNotExist:
            messages.error(
                    request, 
                    message='Prośba o dołączenie drużyny nie istnieje  🤷‍♂️',
                    extra_tags='alert-danger'
                )
            return redirect(reverse_lazy('webapp:index'))

        return redirect(request.META.get('HTTP_REFERER'))


class JoinTeamAcceptance(JoinTeamResponseMixin, View):
    def post(self, request, *args, **kwargs):
        notification_data = super().get_notification_data(request)

        # Handle errors
        if notification_data.get('error_with_redirect'):
            return notification_data['error_with_redirect']

        team_admin = notification_data['team_admin']
        applicant = notification_data['applicant']
        notification_type = notification_data['notification_type']
        join_request_notif = notification_data['join_request_notif']
        
        try:
            team = Team.objects.get(id=request.POST.get('team-id'))
        except Team.DoesNotExist:
            messages.error(
                request, 
                message='Drużyna nie istnieje 🤷‍♂️',
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
            notification_type = notification_type,
            message = f'Gratulacje twoja prośba o dołączenie do drużyny dla {organization_name} została zaakcaptowana!',
            related_url = team.get_absolute_url()
        )

        # Delete the old notification
        join_request_notif.delete()

        # Add message that the aplicant joined your team
        messages.info(
            request, 
            message=format_html(f'Powitaj nowego członka drużyny na <a href="{team.get_absolute_url()}">czacie</a> gdy dołączy 👋'),
            extra_tags='alert-success'
        )

        return redirect(request.META.get('HTTP_REFERER'))



class JoinTeamRejection(JoinTeamResponseMixin, View):
    def post(self, request, *args, **kwargs):
        notification_data = super().get_notification_data(request)

        # Handle errors
        if notification_data.get('error_with_redirect'):
            return notification_data['error_with_redirect']

        team_admin = notification_data['team_admin']
        applicant = notification_data['applicant']
        notification_type = notification_data['notification_type']
        join_request_notif = notification_data['join_request_notif']

        # Get the the team's organization name
        organization_name = join_request_notif.extra_data['organization']

        # Create notification that the user's request got rejected
        Notification.objects.create(
            sender = team_admin, 
            recipient = applicant, 
            notification_type = notification_type,
            message = f'😢 Twoja prośba o dołączenie do drużyny dla {organization_name} została odrzucona. Powodów może być wiele, więc nie zniechęcaj się',
        )

        # Delete the old notification
        join_request_notif.delete()

        return redirect(request.META.get('HTTP_REFERER'))