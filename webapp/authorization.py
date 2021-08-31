from django.contrib.auth.mixins import UserPassesTestMixin


class UserIsOrganizationTestMixin(UserPassesTestMixin):
    def test_func(self):
        return hasattr(self.request.user, 'organization')


class UserIsCreatorTestMixin(UserPassesTestMixin):
    def test_func(self):
        return hasattr(self.request.user, 'creator')