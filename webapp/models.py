from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomAccountManager


class User(AbstractBaseUser,PermissionsMixin):
    objects = CustomAccountManager()

    email = models.EmailField(unique=True, blank=False)
    is_organization = models.BooleanField('is organization?', default=False)
    is_creator = models.BooleanField('is creator?', default=False)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

# class Organization(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     user.is_organization = True
#     name = models.CharField(unique=True, required=True)
#     fb_url = models.URLField(blank=True, null=True)
#     twitter_url = models.URLField(blank=True, null=True)
#     KRS = models.CharField(max_length=10, blank=True, null=True)

# class Creator(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     user.is_creator = True
#     first_name = models.CharField(max_length=150, blank=True, null=True)
#     last_name = models.CharField(max_length=150, blank=True, null=True)