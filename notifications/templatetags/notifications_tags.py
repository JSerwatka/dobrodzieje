
from django import template
from notifications.models import Notification

register = template.Library()

@register.inclusion_tag('notifications/show_notifications.html', takes_context=True)
def show_notifications(context):
	request_user = context['request'].user
	notifications = Notification.objects.filter(receiver=request_user).order_by('-created_on')
	return {'notifications': notifications}