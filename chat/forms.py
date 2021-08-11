from django import forms
from webapp.models import Team
from webapp.models import Roles

class TeamForm(forms.ModelForm):
    our_stack = forms.MultipleChoiceField(label="Jakich technologii używamy", choices=Team.TECHNOLOGIES_CHOICES)
    looking_for = forms.MultipleChoiceField(label="Kogo poszukujemy:", choices=Roles.choices)
    is_closed = forms.BooleanField(label='Zamknięta grupa?')

    class Meta:
        model = Team
        fields = ['is_closed', 'our_stack', 'looking_for']