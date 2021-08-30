from django.contrib.postgres import fields
from django.db.models.enums import Choices
from django.forms import widgets
import django_filters
from django import forms
from .models import Announcement, Organization, Team, Roles, City

class AnnouncementFilter(django_filters.FilterSet):
    ANNOUNCEMENT_STATUS_CHOICES = [
        ('no team', 'Brak drużyny'),
        ('team opened', 'Drużyna otwarta'),
        ('team closed', 'Drużyna zamknięta'),
    ]

    category = django_filters.ChoiceFilter(label='Wybierz kategorię:',
                                           field_name='organization__category', 
                                           choices=Organization.ORGANIZATION_CATEGORY_CHOICES)
    city = django_filters.ModelChoiceFilter(label='Wybierz miasto:', 
                                            field_name='organization__city', 
                                            queryset=City.objects.used_cities())
    stack = django_filters.MultipleChoiceFilter(label='W jakich technologiach chcesz pracować:',
                                                field_name='team__our_stack',
                                                lookup_expr='icontains',
                                                choices=Team.TECHNOLOGIES_CHOICES)
    looking_for = django_filters.MultipleChoiceFilter(label='W jakich roli chcesz pracować:',
                                                      field_name='team__looking_for',
                                                      lookup_expr='icontains',
                                                      choices=Roles.choices)
    announcement_status = django_filters.ChoiceFilter(label='Drużyna:',
                                                      choices=ANNOUNCEMENT_STATUS_CHOICES,
                                                      method='announcement_status_filter')
    #TODO make form fully cripsy - without widget tweaks
    #TODO show only categories, stack, looking_for which are available??

    # stack = django_filters.MultipleChoiceFilter(label='W jakich technologiach chcesz pracować',
    #                                             field_name='team__our_stack',
    #                                             choices=Team.TECHNOLOGIES_CHOICES,
    #                                             widget=forms.Select(attrs={'data-multi-select-plugin': None}))
    # looking_for = django_filters.MultipleChoiceFilter(label='W jakich roli chcesz pracować',
    #                                                   field_name='team__looking_for',
    #                                                   choices=Roles.choices,
    #                                                   widget=forms.Select(attrs={'data-multi-select-plugin': None}))

    class Meta:
        model = Announcement
        fields = ['category']   

    def announcement_status_filter(self, queryset, name, value):
        if value == 'no team':
            return queryset.filter(team__isnull=True)
        elif value == 'team opened':
            return queryset.filter(team__is_closed=False)
        else:
            return queryset.filter(team__is_closed=True)
