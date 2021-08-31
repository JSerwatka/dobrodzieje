
from django import template
from notifications.models import Notification

register = template.Library()

@register.inclusion_tag('notifications/show_notifications.html', takes_context=True)
def show_notifications(context):
	request_user = context['request'].user
	notifications = Notification.objects.filter(recipient=request_user).order_by('-created_on')
	return {'notifications': notifications}

@register.simple_tag(takes_context=True)
def join_request_send(context, join_request_type):
	request_user = context['request'].user
	if join_request_type == 'Announcement':
		notification_type = Notification.NotificationType.JOIN_ANNOUNCEMENT_REQUEST
		recipient = context['announcement'].organization.user
	elif join_request_type == 'Team':
		recipient = context['team'].get_admin()
		notification_type = Notification.NotificationType.JOIN_TEAM_REQUEST
		#TODO check for team id extra data
	return Notification.objects.filter(
				sender=request_user, 
				recipient=recipient, 
				notification_type=notification_type
			).exists()