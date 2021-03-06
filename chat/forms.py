from django import forms
from django.forms import widgets
from webapp.models import Team, TeamMember
from webapp.models import Roles

class TeamForm(forms.ModelForm):
    #TODO make form fully cripsy - without widget tweaks
    our_stack = forms.MultipleChoiceField(label="Jakich technologii używamy", choices=Team.TECHNOLOGIES_CHOICES, required=False)
    looking_for = forms.MultipleChoiceField(label="Kogo poszukujemy:", choices=Roles.choices, required=False)
    is_closed = forms.BooleanField(label='Zamknięta grupa?', required=False)

    class Meta:
        model = Team
        fields = ['is_closed', 'our_stack', 'looking_for']

class JoinTeamAdminForm(forms.ModelForm):
    nick = forms.CharField(label="Jak chcesz się nazywać w drużynie?", required=True)
    role = forms.ChoiceField(label="Wybierz swoją rolę", choices=Roles.choices)

    class Meta:
        model = TeamMember
        fields = ['role', 'nick']

class JoinTeamForm(forms.ModelForm):
    nick = forms.CharField(label="Jak chcesz się nazywać w drużynie?", required=True)

    class Meta:
        model = TeamMember
        fields = ['nick']