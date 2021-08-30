from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Message
from webapp.models import Team

"""
#TODO set proper message and description
@receiver(post_save, sender=Message)
def message_post_save(sender, instance, created, *args, **kwargs):
    if created:
        team = Team.objects.get(id=instance.team_id)
        print('Message handler')
        print("sender", sender)
        print("instance", instance.__dict__)
        # Notify all teammembers besides the sender
        users_to_notify = team.members.exclude(user_id=instance.sender_id)
        print(team.members.__dict__)
        print(users_to_notify)
        print(users_to_notify.__dict__)
        # notify.send(actor=team, recipient=users_to_notify, verb="nowa wiadomość")
"""