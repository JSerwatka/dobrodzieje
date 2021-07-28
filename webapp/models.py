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
    name = models.CharField('organization\'s name', max_length=255, unique=True)
    category = models.CharField(max_length=10, choices=ORGANIZATION_CATEGORY_CHOICES)
    phone_number = models.CharField('phone number', max_length=9, blank=True, null=True)
    fb_url = models.URLField('facebook page URL', blank=True, null=True)
    twitter_url = models.URLField('twitter accout URL', blank=True, null=True)
    KRS = models.CharField(max_length=10, blank=True, null=True)
    #TODO miejscowość
    #TODO województwo


class Creator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user.is_creator = True
    first_name = models.CharField('first name', max_length=150, blank=True, null=True)
    last_name = models.CharField('last name', max_length=150, blank=True, null=True)


class Announcement(models.Model):
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE)
    logo = models.ImageField('organization\'s logo', upload_to='logos/', blank=True, null=True)
    #TODO co należy zrobić?
    #TODO zdjęcia przyszłej strony??
    old_website = models.URLField('previous organization\'s website', blank=True, null=True)
    created_on = models.DateTimeField('created on', auto_now_add=True)


class Team(models.Model):
    pass


class TeamMember(models.Model):

    ROLE_CHOICES = [
        ('FE', 'Front-End Developer'),
        ('FS', 'Full-Stack Developer'),
        ('BE', 'Back-End Developer'),
        ('GD', 'Graphic Designer')
    ]

    creator = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='teams')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="members")
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)
    is_admin = models.BooleanField('is admin?', default=False)


