from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Organization, Creator
from django.db import transaction

class OrganizationRegisterForm(UserCreationForm):
    name = forms.CharField(required=True)
    category = forms.ChoiceField(choices=Organization.ORGANIZATION_CATEGORY_CHOICES)
    phone_number = forms.CharField(required=False)
    fb_url = forms.URLField(required=False)
    twitter_url = forms.URLField(required=False)
    KRS = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.save()
        organization = Organization(user=user)
        organization.name = self.cleaned_data.get('name')
        organization.category = self.cleaned_data.get('category')
        organization.phone_number = self.cleaned_data.get('phone_number')
        organization.fb_url = self.cleaned_data.get('fb_url')
        organization.twitter_url = self.cleaned_data.get('twitter_url')
        organization.KRS = self.cleaned_data.get('KRS')
        organization.save()
        return user


class CreatorRegisterForm(UserCreationForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.save()
        creator = Creator(user=user)
        creator.first_name = self.cleaned_data.get('first_name')
        creator.last_name = self.cleaned_data.get('last_name')
        creator.save()
        return user
