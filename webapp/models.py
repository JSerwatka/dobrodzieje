from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomAccountManager, AnnouncementQuerySetManager
from django.contrib.postgres.fields import ArrayField
from ckeditor.fields import RichTextField

from django.contrib import admin
from django.urls import reverse


# ===== Choices =====
# info https://docs.djangoproject.com/en/3.2/ref/models/fields/#enumeration-types
class Roles(models.TextChoices):
    FRONTEND = ('FE', 'Front-End Developer')
    FULLSTACK = ('FS', 'Full-Stack Developer')
    BACKEND = ('BE', 'Back-End Developer')
    DESIGNER = ('GD', 'Graphic Designer')



# ===== Models =====
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

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField('organization\'s name', max_length=255, unique=True)
    category = models.CharField(max_length=10, choices=ORGANIZATION_CATEGORY_CHOICES)
    phone_number = models.CharField('phone number', max_length=9, blank=True, null=True)
    fb_url = models.URLField('facebook page URL', blank=True, null=True)
    twitter_url = models.URLField('twitter accout URL', blank=True, null=True)
    KRS = models.CharField(max_length=10, blank=True, null=True)
    #TODO miejscowość
    #TODO województwo

    def __str__(self):
        return self.name


class Creator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField('first name', max_length=150, blank=True, null=True)
    last_name = models.CharField('last name', max_length=150, blank=True, null=True)


    def __str__(self):
        return f'{self.user}' + \
               (f' ({self.last_name}, {self.first_name})' if (self.first_name and self.last_name) else '')


class Announcement(models.Model):
    objects = AnnouncementQuerySetManager().as_manager()

    organization = models.OneToOneField(Organization, on_delete=models.CASCADE)
    logo = models.ImageField('organization\'s logo', upload_to='logos/', blank=True, null=True)
    content = RichTextField('what needs to be done', blank=False, null=False)
    #TODO zdjęcia przyszłej strony??
    old_website = models.URLField('previous organization\'s website', blank=True, null=True)
    created_on = models.DateTimeField('created on', auto_now_add=True)

    def __str__(self):
        return f'Announcement by {self.organization}'

    def get_absolute_url(self):
        return reverse('announcement-detail', kwargs={'id': self.id}) 

class Team(models.Model):

    TECHNOLOGIES_CHOICES = [
        ('PY', 'python'),
        ('NJS', 'node.js'),
        ('PHP', 'php'),
        ('ROR', 'ruby on rails'),
        ('JSP', 'java'),
        ('ASX', '.net'),
        ('GO', 'golang'),
        ('HC', 'html&css'),
        ('JS', 'javascript'),
        ('TS', 'typescript'),
        ('JSX', 'react'),
        ('ANG', 'angular'),
        ('VUE', 'vue.js'),
        ('CPP', 'c++'),
        ('C', 'c'),
        ('RN', 'react native'),
        ('FL', 'flutter'),
        ('SC', 'scala'),
        ('EX', 'elixir'),
        ('KT', 'kotlin')
    ]


    announcement = models.OneToOneField(Announcement, on_delete=models.CASCADE)
    is_closed = models.BooleanField('is closed?', default=False)
    members = models.ManyToManyField(Creator, related_name='teams', through='TeamMember')
    # info https://docs.djangoproject.com/en/dev/ref/contrib/postgres/fields/#arrayfield
    our_stack = ArrayField(
        models.CharField('What technologies we use?', max_length=3, choices=TECHNOLOGIES_CHOICES),
        blank=True, 
        null=True
    )
    looking_for = ArrayField(
        models.CharField('looking for those roles', max_length=2, choices=Roles.choices),
        blank=True, 
        null=True
    )
    #TODO chat foreign key

    def __str__(self):
        return f'Team for {self.announcement}'


# Jak używać many to many https://youtu.be/-HuTlmEVOgU?t=890
class TeamMember(models.Model):
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.CharField(max_length=2, choices=Roles.choices)
    is_admin = models.BooleanField('is admin?', default=False)

    @admin.display(description='Creator')
    def get_creator_str(self):
        return str(self.creator)    
        
    @admin.display(description='Team')
    def get_team_str(self):
        return str(self.team)

    class Meta:
        unique_together = ['creator', 'team']


#TODO Notifications model
#TODO Chat model
#TODO Message model