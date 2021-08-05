from django.contrib.postgres import fields
import django_filters
from .models import Announcement, Organization, Team

class AnnouncementFilter(django_filters.FilterSet):
    category = django_filters.ChoiceFilter(label='Wybierz kategorię',
                                           field_name='organization__category', 
                                           choices=Organization.ORGANIZATION_CATEGORY_CHOICES)

    class Meta:
        model = Announcement
        fields = ['category']
