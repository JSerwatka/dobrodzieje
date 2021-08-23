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
    DeleteView,
    ListView
)
from .models import (
    Announcement, 
    Organization, 
    User,
    Creator,
    Team
)

from .forms import (
    OrganizationRegisterForm,
    CreatorRegisterForm,
    AnnouncementForm,
    OrganizationEditForm,
    CreatorEditForm
)

from .filters import (
    AnnouncementFilter,
)


# ==== Basic ===== 
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


# ==== Announcement ===== 
class AnnouncementList(ListView):
    template_name = 'webapp/announcemenet_list.html'
    context_object_name = 'announcements'
    paginate_by = 10 

    # def dispatch(self, request, *args, **kwargs):
    #     self.filter_organization = None  # Will be set in get_queryset()
    #     return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar_active'] = 'announcement-list'
        context['filter_announcements'] = self.filter_announcements
        return context

    def get_queryset(self):
        qs = Announcement.objects.select_related('organization').order_by('created_on')
        self.filter_announcements = AnnouncementFilter(self.request.GET, queryset=qs)
        voivodeship_id = self.request.GET.get('voivodeship')
        if voivodeship_id:
            output_qs = self.filter_announcements.qs.filter(organization__city__voivodeship_id=voivodeship_id)
        else:
            output_qs = self.filter_announcements.qs
        return output_qs


class AnnouncementDetails(DetailView):
    template_name = 'webapp/announcement_detail.html'
    context_object_name = 'announcement'

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Announcement, id=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #TODO why this works without knowing announcement id?
        is_author = Announcement.objects.is_author(self.request.user)
        context['is_author'] = is_author
        #TODO context['is_team'] -> allow to open group/with organization chat
        #TODO context['is_creator'] -> join group/create group and contact organization chat buttons
        context['is_creator'] = self.request.user.is_creator
        context['navbar_active'] = 'my-announcement' if is_author else None
        return context


class MyAnnouncement(TemplateView):
    template_name = 'webapp/announcement_empty.html'

    def get(self, request, *args, **kwargs):
        announcement = Announcement.objects.for_user(request.user)
        if announcement:
            return redirect(reverse_lazy('webapp:announcement-detail', kwargs={'id': announcement.id}))

        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar_active'] = 'my-announcement'
        return context


class AnnouncementCreate(CreateView):
    template_name = 'webapp/announcement_edit.html'
    form_class = AnnouncementForm

    def form_valid(self, form):
        form.instance.organization = self.request.user.organization
        return super().form_valid(form)

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['organization'] = self.request.user.organization
        return context


class AnnouncementUpdate(UpdateView):
    template_name = 'webapp/announcement_edit.html'
    form_class = AnnouncementForm

    def get_object(self):
        return Announcement.objects.for_user_or_400(self.request.user)

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['organization'] = self.request.user.organization
        return context


class AnnouncementDelete(DeleteView):
    template_name = 'webapp/announcemenet_delete.html'
    success_url = reverse_lazy('webapp:index')
    
    def get_object(self):
        return Announcement.objects.for_user_or_400(self.request.user)


# ==== Teams ===== 
class MyTeams(ListView):
    template_name = 'webapp/teams_list.html'
    context_object_name = 'teams'
    #TODO paginate_by = 10 
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar_active'] = 'my-teams'
        return context

    def get_queryset(self):
        return Team.objects.filter(members__user=self.request.user).select_related('announcement').prefetch_related('teammember_set')

# ==== Edit Profile ===== 
class EditProfile(UpdateView):
    template_name = 'webapp/edit_profile.html'

    def get_form_class(self):
        if self.request.user.is_organization:
            return OrganizationEditForm
        elif self.request.user.is_creator:
            return CreatorEditForm

    def get_object(self):
        if self.request.user.is_organization:
            return self.request.user.organization
        elif self.request.user.is_creator:
            return self.request.user.creator

    def get_success_url(self):
        return reverse_lazy('webapp:index')


# ==== Authentication ===== 
class Login(LoginView):
    template_name = 'webapp/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar_active'] = 'login'
        return context


# Forces all regsiter views to activate "Zarejestruj się" navbar item
class RegisterContextMixin():
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar_active'] = 'register'
        return context


class Register(RegisterContextMixin, TemplateView):
    template_name = 'webapp/register.html'


class RegisterCreator(RegisterContextMixin, CreateView):
    model = User
    template_name = 'webapp/register_creator.html'
    form_class = CreatorRegisterForm
    success_url = reverse_lazy('webapp:index')

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
        new_user = authenticate(email=email, password=password)
        login(self.request, new_user)
        return valid_form


class RegisterOrganization(RegisterContextMixin, CreateView):
    model = User
    template_name = 'webapp/register_organization.html'
    form_class = OrganizationRegisterForm
    success_url = reverse_lazy('webapp:index')

    def form_valid(self, form):
        valid_form = super().form_valid(form)
        email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
        new_user = authenticate(email=email, password=password)
        login(self.request, new_user)
        return valid_form


class Logout(RedirectView):
    url = reverse_lazy('webapp:index')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)