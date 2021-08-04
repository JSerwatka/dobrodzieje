# from django.views.generic.base import RedirectView
# from django.views.generic.detail import DetailView
# from django.views.generic.edit import CreateView, DeleteView
# from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages

from django.views.generic import (
    TemplateView,
    RedirectView,
    DetailView,
    CreateView, 
    UpdateView,
    DeleteView
)
from .models import Announcement, User
from .forms import (
    OrganizationRegisterForm,
    CreatorRegisterForm,
    AnnouncementForm
)


# Create your views here.
class Index(TemplateView):
    template_name = 'webapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar_active'] = 'index'
        return context


# ==== Announcement ===== 
class AnnouncementDetails(DetailView):
    template_name = 'webapp/announcement_detail.html'
    context_object_name = 'announcement'

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Announcement, id=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = Announcement.objects.is_author(self.request.user)
        #TODO context['is_team'] -> allow to open group/with organization chat
        #TODO context['is_creator'] -> join group/create group and contact organization chat buttons
        return context


class MyAnnouncement(TemplateView):
    template_name = 'webapp/announcement_empty.html'

    def get(self, request, *args, **kwargs):
        announcement = Announcement.objects.for_user(request.user)
        if announcement:
            return redirect(reverse_lazy('announcement-detail', kwargs={'id': announcement.id}))

        return super().get(request, *args, **kwargs)


class AnnouncementCreate(CreateView):
    template_name = 'webapp/announcement_edit.html'
    form_class = AnnouncementForm

    def form_valid(self, form):
        form.instance.organization = self.request.user.organization
        return super().form_valid(form)


class AnnouncementUpdate(UpdateView):
    template_name = 'webapp/announcement_edit.html'
    form_class = AnnouncementForm

    def get_object(self):
        return Announcement.objects.for_user_or_400(self.request.user)


class AnnouncementDelete(DeleteView):
    template_name = 'webapp/announcemenet_delete.html'
    success_url = reverse_lazy('index')
    
    def get_object(self):
        return Announcement.objects.for_user_or_400(self.request.user)


# ==== Authentication ===== 
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