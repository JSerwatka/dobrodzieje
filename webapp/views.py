from django.views.generic.edit import CreateView
from webapp.models import Organization
from django.shortcuts import render
from django.urls import reverse_lazy

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


class Login(TemplateView):
    template_name = 'webapp/index.html'


class Register(TemplateView):
    template_name = 'webapp/register.html'


class RegisterCreator(CreateView):
    model = User
    template_name = 'webapp/register_creator.html'
    form_class = CreatorRegisterForm
    success_url = reverse_lazy('index')


class RegisterOrganization(CreateView):
    model = User
    template_name = 'webapp/register_organization.html'
    form_class = OrganizationRegisterForm
    success_url = reverse_lazy('index')