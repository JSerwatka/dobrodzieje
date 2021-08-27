from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Announcement, Team, TeamMember
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
    
@receiver(pre_delete, sender=Announcement)
def announcement_pre_delete(sender, instance, *args, **kwargs):
    # Check if the announcement has a team
    if hasattr(instance, 'team'):
        team_members = instance.team.members.all()
        organization = instance.organization

        for creator in team_members:
            Notification.objects.create(
                sender = organization.user,
                recipient = creator.user, 
                notification_type = Notification.NotificationType.DELETION,
                message = f'Ogłoszenie organizacji {organization} zostało usunięte'
            )

@receiver(pre_delete, sender=TeamMember)
def teammember_pre_delete(sender, instance, *args, **kwargs):
    team = instance.team
    deleted_member = instance.creator.user
    team_admin = team.get_admin()
    organization = team.announcement.organization
    print(deleted_member, team_admin, organization)

    Notification.objects.create(
        sender = team_admin,
        recipient = deleted_member, 
        notification_type = Notification.NotificationType.DELETION,
        message = f'😫 Zostałeś usunięty z drużyny dla organizacji {organization}'
    )