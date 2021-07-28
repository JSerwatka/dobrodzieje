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

class Organization(models.Model):

    ORGANIZATION_CATEGORY_CHOICES = [
        ('DP', 'Działalnośc prospołeczna'),
        ('EiW', 'Edukacja i wychowanie'),
        ('WON', 'Wspanie osób niepełnosprawnych'),
        ('KSiT', 'Kultura, Sztuka i Technologia'),
        ('OZiZ', 'Ochrona zdrowia i życia'),
        ('DCh', 'Działalność charytatywna'),
        ('PDzi', 'Pomoc Dzieciom'),
        ('SiR', 'Sport i rekreacja'),
        ('OSiPZ', 'Ochorna środowiska i praw zwierząt')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user.is_organization = True
    name = models.CharField('organization\'s name', max_length=255, unique=True, blank=False, null=False)
    category = models.CharField(max_length=10, choices=ORGANIZATION_CATEGORY_CHOICES, blank=False, null=False)
    phone_number = models.CharField('phone number', max_length=9, blank=True, null=True)
    fb_url = models.URLField('facebook page URL', blank=True, null=True)
    twitter_url = models.URLField('twitter accout URL', blank=True, null=True)
    KRS = models.CharField(max_length=10, blank=True, null=True)

class Creator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user.is_creator = True
    first_name = models.CharField('first name', max_length=150, blank=True, null=True)
    last_name = models.CharField('last name', max_length=150, blank=True, null=True)