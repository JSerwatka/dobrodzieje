from django.db import models
from django.db.models.fields.json import JSONField
from webapp.models import User


class Notification(models.Model):
    class NotificationType(models.IntegerChoices):
        NEW_MESSAGE = 1, 'New Message'
        JOIN_ANNOUNCEMENT_REQUEST = 2, 'Join Announcement Request'
        JOIN_TEAM_REQUEST = 3, 'Join Team Request'
        JOIN_RESPONSE = 4, 'Join Response'
        DELETION = 5, 'Deletion'


    notification_type = models.IntegerField(choices=NotificationType.choices)
    sender = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    related_url = models.URLField('related url', max_length=255, null=True, blank=True)
    created_on = models.DateTimeField('created on', auto_now_add=True)
    read = models.BooleanField(default=False)
    extra_data = JSONField(blank=True, null=True)