from django.db import models
from webapp.models import User


class Notification(models.Model):
    class NotificationType(models.IntegerChoices):
        NEW_MESSAGE = 1, 'New Message'
        JOIN_REQUEST = 2, 'Join Request'
        JOIN_RESPONSE = 3, 'Join Response'
        DELETION = 4, 'Deletion'


    notification_type = models.IntegerField(choices=NotificationType.choices)
    sender = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    related_url = models.URLField('related url', max_length=255, null=True, blank=True)
    created_on = models.DateTimeField('created on', auto_now_add=True)
    read = models.BooleanField(default=False)