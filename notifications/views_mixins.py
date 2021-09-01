from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages

from webapp.models import (
    Announcement,
    User,
)

from .models import Notification


class JoinAnnouncementMixin:
    def get_notification_data(self, request):
        try:
            sender = request.user
            recipient = User.objects.get(id=request.POST.get('organization'))
            notification_type = Notification.NotificationType.JOIN_ANNOUNCEMENT_REQUEST

            test_announcement = recipient.organization.announcement
            if hasattr(test_announcement, 'team'):
                messages.error(
                    request, 
                    message='Organizacja już ma drużynę 🤷‍♂️',
                    extra_tags='alert-danger'
                )
                return {'error_with_redirect': redirect(reverse_lazy('webapp:index'))}
        except User.DoesNotExist:
            messages.error(
                request, 
                message='Organizacja nie istnieje 🤷‍♂️',
                extra_tags='alert-danger'
            )
            return {'error_with_redirect': redirect(reverse_lazy('webapp:index'))}
        except Announcement.DoesNotExist:
            messages.error(
                request, 
                message='Organizacja nie posiada ogłoszenia 🤷‍♂️',
                extra_tags='alert-danger'
            )
            return {'error_with_redirect': redirect(reverse_lazy('webapp:index'))}

        return {'sender': sender, 'recipient': recipient, 'notification_type': notification_type}


class JoinAnnouncementResponseMixin:
    def get_notification_data(self, request):
        try:
            # Get data from the form
            organization_user = request.user
            creator_user = User.objects.get(id=request.POST.get('creator'))
            notification_type = Notification.NotificationType.JOIN_RESPONSE

            # Check if join request from this user exists
            join_request_notif = Notification.objects.get(sender=creator_user, 
                                                          recipient=organization_user, 
                                                          notification_type=Notification.NotificationType.JOIN_ANNOUNCEMENT_REQUEST)
        except User.DoesNotExist:
            messages.error(
                request, 
                message='Użytkownik nie istnieje nie istnieje 🤷‍♂️',
                extra_tags='alert-danger'
            )
            return {'error_with_redirect': redirect(reverse_lazy('webapp:index'))}
        except Notification.DoesNotExist:
            messages.error(
                request, 
                message='Ten użytkownik nie wysłał prośby o stworzenie drużyny 🤷‍♂️',
                extra_tags='alert-danger'
            )
            return {'error_with_redirect': redirect(reverse_lazy('webapp:index'))}
        
        return {
            'organization_user': organization_user, 
            'creator_user': creator_user, 
            'notification_type': notification_type,
            'join_request_notif': join_request_notif
        }
