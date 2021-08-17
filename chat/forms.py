from django import forms
from django.forms import widgets
from webapp.models import Team
from webapp.models import Roles

class TeamForm(forms.ModelForm):
    our_stack = forms.MultipleChoiceField(label="Jakich technologii używamy", choices=Team.TECHNOLOGIES_CHOICES, required=False)
    # our_stack = forms.MultipleChoiceField(label="Jakich technologii używamy", choices=Team.TECHNOLOGIES_CHOICES, required=False, widget=forms.Select(attrs={'data-multi-select-plugin': None}))
    looking_for = forms.MultipleChoiceField(label="Kogo poszukujemy:", choices=Roles.choices, required=False)
    # looking_for = forms.MultipleChoiceField(label="Kogo poszukujemy:", choices=Roles.choices, required=False, widget=forms.Select(attrs={'data-multi-select-plugin': None}))
    is_closed = forms.BooleanField(label='Zamknięta grupa?', required=False)

    class Meta:
        model = Team
        fields = ['is_closed', 'our_stack', 'looking_for']