from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets
from .models import User, Organization, Creator
from django.db import transaction

class OrganizationRegisterForm(UserCreationForm):
    name = forms.CharField(required=True, label='Nazwa organizacji',
                           widget=forms.TextInput(attrs={'aria-label': 'Podaj nazwę organizacji'}))
    category = forms.ChoiceField(choices=Organization.ORGANIZATION_CATEGORY_CHOICES, label='Kategoria', 
                                 widget=forms.Select(attrs={'aria-label': 'Wybierz kategorię'}))
    phone_number = forms.CharField(required=False, label='Numer telefonu', max_length=9,
                                   widget=forms.TextInput(attrs={'aria-label': 'Wpisz numer telefonu'}))
    fb_url = forms.URLField(required=False, label='Strona na Facebook', 
                            widget=forms.URLInput(attrs={
                                'placeholder': 'Wpisz adres strony (np. https://www.facebook.com/PolskaAkcjaHumanitarna/)',
                                'aria-label': 'Wpisz adres strony (np. https://www.facebook.com/PolskaAkcjaHumanitarna/)'
                            }))
    twitter_url = forms.URLField(required=False, label='Konto na Twitter', 
                                 widget=forms.URLInput(attrs={
                                     'placeholder': 'Wpisz adres strony (np. https://twitter.com/PAH_org)',
                                     'aria-label': 'Wpisz adres strony (np. https://twitter.com/PAH_org)'
                                 }))
    KRS = forms.CharField(required=False, label='Numer KRS', max_length=10,
                          widget=forms.TextInput(attrs={'aria-label': 'Podaj numer KRS'}))

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
        return 
        
    def clean(self):
        cleaned_data = super().clean()

        fb_url = cleaned_data.get('fb_url')
        twitter_url = cleaned_data.get('twitter_url')

        if fb_url:
            if 'facebook.com' not in fb_url:
                self.add_error('fb_url', 'Podany adres nie należy do Facebook\'a') 
        
        if twitter_url:
            if 'twitter.com' not in twitter_url:
                self.add_error('twitter_url', 'Podany adres nie należy do Twitter\'a') 

        return cleaned_data


class CreatorRegisterForm(UserCreationForm):
    first_name = forms.CharField(required=False, label='Imię',
                                 widget=forms.TextInput(attrs={'aria-label': 'Podaj imię'}))
    last_name = forms.CharField(required=False, label='Nazwisko',
                                widget=forms.TextInput(attrs={'aria-label': 'Podaj nazwisko'}))

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
