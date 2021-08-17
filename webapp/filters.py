from django.contrib.postgres import fields
from django.db.models.enums import Choices
from django.forms import widgets
import django_filters
from django import forms
from .models import Announcement, Organization, Team, Roles, City

class AnnouncementFilter(django_filters.FilterSet):
    category = django_filters.ChoiceFilter(label='Wybierz kategorię',
                                           field_name='organization__category', 
                                           choices=Organization.ORGANIZATION_CATEGORY_CHOICES)
    city = django_filters.ModelChoiceFilter(label='Miasto', 
                                            field_name='organization__city', 
                                            queryset=City.objects.used_cities())
    stack = django_filters.MultipleChoiceFilter(label='W jakich technologiach chcesz pracować',
                                                field_name='team__our_stack',
                                                lookup_expr='icontains',
                                                choices=Team.TECHNOLOGIES_CHOICES)
    looking_for = django_filters.MultipleChoiceFilter(label='W jakich roli chcesz pracować',
                                                      field_name='team__looking_for',
                                                      lookup_expr='icontains',
                                                      choices=Roles.choices)
    #TODO make form fully cripsy - without widget tweaks
    # TODO show only categories, stack, looking_for which are available??

    # stack = django_filters.MultipleChoiceFilter(label='W jakich technologiach chcesz pracować',
    #                                             field_name='team__our_stack',
    #                                             choices=Team.TECHNOLOGIES_CHOICES,
    #                                             widget=forms.Select(attrs={'data-multi-select-plugin': None}))
    # looking_for = django_filters.MultipleChoiceFilter(label='W jakich roli chcesz pracować',
    #                                                   field_name='team__looking_for',
    #                                                   choices=Roles.choices,
    #                                                   widget=forms.Select(attrs={'data-multi-select-plugin': None}))
    is_closed = django_filters.BooleanFilter(label='Czy grupa jest zamknięta',
                                             field_name='team__is_closed')
    #TODO 
    class Meta:
        model = Announcement
        fields = ['category']   


# class TeamFilter(django_filters.FilterSet):
#     our_stack = 