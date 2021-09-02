from django.contrib.auth.mixins import UserPassesTestMixin
from webapp.models import Team, TeamMember


class UserIsTeamMemberTestMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_anonymous:
            return False
        return TeamMember.objects.filter(team__id=self.kwargs.get('team_id'), creator=self.request.user.creator).exists()


class UserIsTeamMemberAdminTestMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_anonymous:
            return False
        
        team_admin = Team.objects.get(id=self.kwargs.get('team_id')).get_admin()

        return team_admin == self.request.user