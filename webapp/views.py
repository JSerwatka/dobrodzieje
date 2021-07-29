from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView
from webapp.models import Organization
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.views import LoginView

from django.views.generic import (
    TemplateView, 
    FormView
)
from .models import User
from .forms import (
    OrganizationRegisterForm,
    CreatorRegisterForm
)


# Create your views here.
class Index(TemplateView):
    template_name = 'webapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar_active'] = 'index'
        return context



class ForCreators(TemplateView):
    template_name = 'webapp/for_creators.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar_active'] = 'for-creators'
        return context


class ForOrganizations(TemplateView):
    template_name = 'webapp/for_organizations.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar_active'] = 'for-organizations'
        return context


class Login(LoginView):
    template_name = 'webapp/login.html'


class Register(TemplateView):
    template_name = 'webapp/register.html'


class RegisterCreator(CreateView):
    model = User
    template_name = 'webapp/register_creator.html'
    form_class = CreatorRegisterForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        print(form.cleaned_data)
        email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
        new_user = authenticate(email=email, password=password)
        login(self.request, new_user)
        return valid_form


class RegisterOrganization(CreateView):
    model = User
    template_name = 'webapp/register_organization.html'
    form_class = OrganizationRegisterForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
        new_user = authenticate(email=email, password=password)
        login(self.request, new_user)
        return valid_form


class Logout(RedirectView):
    url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)