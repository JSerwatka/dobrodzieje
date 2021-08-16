from django.contrib.postgres import fields
from django.db.models.enums import Choices
import django_filters
from .models import Announcement, Organization, Team, Roles

class AnnouncementFilter(django_filters.FilterSet):
    category = django_filters.ChoiceFilter(label='Wybierz kategorię',
                                           field_name='organization__category', 
                                           choices=Organization.ORGANIZATION_CATEGORY_CHOICES)
    # stack = django_filters.MultipleChoiceFilter(label='W jakich technologiach chcesz pracować',
    #                                     field_name='announcement__team__our_stack',
    #                                     choices=Team.TECHNOLOGIES_CHOICES)
    # looking_for = django_filters.MultipleChoiceFilter(label='W jakich roli chcesz pracować',
    #                                     field_name='team__looking_for',
    #                                     choices=Roles.choices)
    # is_closed = django_filters.BooleanFilter(label='Czy grupa jest zamknięta',
    #                                     field_name='team__is_closed')
    class Meta:
        model = Announcement
        fields = ['category']   

# class TeamFilter(django_filters.FilterSet):
#     our_stack = 