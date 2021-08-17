from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.core.exceptions import BadRequest


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password, **other_fields):

        if not email:
            raise ValueError("You must provide an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user


class AnnouncementQuerySetManager(models.QuerySet):
    def for_user(self, user):
        return self.filter(organization__user__email=user).first()

    def is_author(self, user):
        return True if self.filter(organization__user__email=user).first() else False

    def for_user_or_400(self, user):
        announcement = self.for_user(user=user)
        if announcement is None:
            raise BadRequest('Invalid request.')
        return announcement


class CityManager(models.Manager):
    def used_cities(self):
        from .models import Organization

        ids = Organization.objects.filter(city__isnull=False).values_list('city', flat=True)
        return self.filter(id__in=ids)
