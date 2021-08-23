from django.db import models


class Message(models.Model):
    team = models.ForeignKey('webapp.Team', on_delete=models.CASCADE)
    sender = models.ForeignKey('webapp.User', on_delete=models.CASCADE)
    content = models.TextField(blank=False, null=False, verbose_name='message content')
    created_on = models.DateTimeField('created on', auto_now_add=True)

    class Meta:
        ordering = ('-created_on',)

