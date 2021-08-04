from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Organization, Announcement

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         if instance.is_organization:
#             Organization.objects.create(user=instance)
#         elif instance.is_creator:
#             Creator.objects.create(user=instance)

# @receiver(pre_save, sender=Announcement)
# def save_announcement(sender, instance, **kwargs):
#     print('-------------------')
#     print(instance)
#     print(sender)
#     print(kwargs)