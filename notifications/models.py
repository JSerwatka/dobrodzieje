from django.db import models


# Create your models here.
class Notification(models.Model):
    class NotificationType(models.IntegerChoices):
        NEW_MESSAGE = 1, 'New Message'
        JOIN_REQUEST = 2, 'Join Request'
        JOIN_RESPONSE = 3, 'Join Response'
        DELETION = 4, 'Deletion'


    type = models.IntegerField(choices=NotificationType.choices)
    sender = models.ForeignKey('webapp.User', related_name='notification_from', on_delete=models.CASCADE)
    receiver = models.ForeignKey('webapp.User', related_name='notification_to', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    related_url = models.URLField('related url', max_length=255)
    created_on = models.DateTimeField('created on', auto_now_add=True)
    read = models.BooleanField(default=False)