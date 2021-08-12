from django import forms
from webapp.models import Team
from webapp.models import Roles

class TeamForm(forms.ModelForm):
    our_stack = forms.MultipleChoiceField(label="Jakich technologii używamy", choices=Team.TECHNOLOGIES_CHOICES, required=False)
    looking_for = forms.MultipleChoiceField(label="Kogo poszukujemy:", choices=Roles.choices, required=False)
    is_closed = forms.BooleanField(label='Zamknięta grupa?', required=False)

    class Meta:
        model = Team
        fields = ['is_closed', 'our_stack', 'looking_for']