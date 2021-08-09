from django.db import models
from webapp.models import Team, User

# Create your models here.
class Message(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=False, null=False, verbose_name='message content')
    created_on = models.DateTimeField('created on', auto_now_add=True)

    class Meta:
        ordering = ('created_on',)