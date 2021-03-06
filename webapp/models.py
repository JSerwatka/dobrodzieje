from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from ckeditor.fields import RichTextField
from django.contrib import admin
from django.urls import reverse
from .managers import (
    CustomAccountManager, 
    AnnouncementQuerySetManager, 
    CityManager
)

import bleach


# Set ckeditor sanitizing rules
bleach.sanitizer.ALLOWED_TAGS += ['p', 'span', 'u', 'ul', 'ol', 'hr', 'img' ,'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6','pre', 'address', 'strong', 'br']
bleach.sanitizer.ALLOWED_ATTRIBUTES.update({'*': ['style'], 'img': ['alt', 'src']})
bleach.sanitizer.ALLOWED_STYLES += ['color', 'font-size', 'text-align', 'list-style-type', 'background-color', 'height', 'width', 'margin-left', 'float', 'margin', 'border-width', 'border-style']

# ===== Choices =====
# info https://docs.djangoproject.com/en/3.2/ref/models/fields/#enumeration-types
class Roles(models.TextChoices):
    FRONTEND = ('FE', 'Front-End Developer')
    FULLSTACK = ('FS', 'Full-Stack Developer')
    BACKEND = ('BE', 'Back-End Developer')
    DESIGNER = ('GD', 'Graphic Designer')

    @classmethod
    def get_labels_by_values(cls, values):
        return [role_name for (role_value, role_name) in Roles.choices if role_value in values]


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


class Voivodeship(models.Model):
    name = models.CharField(max_length=255,  unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    objects = CityManager()

    voivodeship = models.ForeignKey(Voivodeship, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Cities'
        ordering = ('name',)
        unique_together = ['voivodeship', 'name']

    def __str__(self):
        return self.name


class Organization(models.Model):
    ORGANIZATION_CATEGORY_CHOICES = [
        ('DP', 'Dzia??alno??c prospo??eczna'),
        ('EiW', 'Edukacja i wychowanie'),
        ('WON', 'Wspanie os??b niepe??nosprawnych'),
        ('KSiT', 'Kultura, Sztuka i Technologia'),
        ('OZiZ', 'Ochrona zdrowia i ??ycia'),
        ('DCh', 'Dzia??alno???? charytatywna'),
        ('PDzi', 'Pomoc Dzieciom'),
        ('SiR', 'Sport i rekreacja'),
        ('OSiPZ', 'Ochorna ??rodowiska i praw zwierz??t')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField('organization\'s name', max_length=255, unique=True)
    category = models.CharField(max_length=10, choices=ORGANIZATION_CATEGORY_CHOICES)
    phone_number = models.CharField('phone number', max_length=9, blank=True, null=True)
    fb_url = models.URLField('facebook page URL', blank=True, null=True)
    twitter_url = models.URLField('twitter accout URL', blank=True, null=True)
    KRS = models.CharField(max_length=10, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)

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
    objects = AnnouncementQuerySetManager.as_manager()

    organization = models.OneToOneField(Organization, on_delete=models.CASCADE)
    logo = models.ImageField('organization\'s logo', upload_to='logos/', blank=True, null=True)
    content = RichTextField('what needs to be done', blank=False, null=False)
    #TODO images of the future website??
    old_website = models.URLField('previous organization\'s website', blank=True, null=True)
    created_on = models.DateTimeField('created on', auto_now_add=True)

    def __str__(self):
        return f'Announcement by {self.organization}'

    def get_absolute_url(self):
        return reverse('webapp:announcement-detail', kwargs={'id': self.id})

    def is_author(self, user):
        return self.organization.user == user

    def save(self, *args, **kwargs):
        self.content = bleach.clean(self.content)
        super().save(*args, **kwargs)


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

    def __str__(self):
        return f'Team for {self.announcement}'

    def get_absolute_url(self):
        return reverse("chat:team-chat", kwargs={"team_id": self.id})

    def get_admin(self):
        return self.teammember_set.get(is_admin=True).creator.user


# Jak u??ywa?? many to many https://youtu.be/-HuTlmEVOgU?t=890
class TeamMember(models.Model):
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.CharField(max_length=2, choices=Roles.choices, null=True)
    is_admin = models.BooleanField('is admin?', default=False)
    nick = models.CharField(max_length=50, null=True)
    joined = models.BooleanField('user joined?', default=False)

    @admin.display(description='Creator')
    def show_creator(self):
        return str(self.creator)    

    @admin.display(description='Team')
    def show_team(self):
        return str(self.team)

    class Meta:
        unique_together = ['creator', 'team']