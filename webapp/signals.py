from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Team
from notifications.models import Notification

@receiver(pre_delete, sender=Team)
def team_pre_delete(sender, instance, *args, **kwargs):
    team_members = instance.members.all()
    team_admin = instance.teammember_set.get(is_admin=True).creator.user
    organization = instance.announcement.organization

    for creator in team_members:
        Notification.objects.create(
            sender = team_admin,
            recipient = creator.user, 
            notification_type = Notification.NotificationType.DELETION,
            message = f'Twoja drużyna do organizacji {organization} została usunięta'
        )