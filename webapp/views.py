from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.views.generic import (
    TemplateView,
    RedirectView,
    DetailView,
    CreateView, 
    UpdateView,
    DeleteView,
    ListView
)
from django.contrib.auth.mixins import LoginRequiredMixin

from .authorization import (
    UserIsOrganizationTestMixin,
    UserIsCreatorTestMixin
)
from .models import (
    Announcement, 
    User,
    Team
)
from .forms import (
    OrganizationRegisterForm,
    CreatorRegisterForm,
    AnnouncementForm,
    OrganizationEditForm,
    CreatorEditForm,
    TeamJoinForm
)
from .filters import AnnouncementFilter


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
class AnnouncementStateContextMixin:
    def get_announcement_state(self, announcement):
        context = {}
        # Check if the announcement has a team
        if hasattr(announcement, 'team'):
            team = announcement.team
            is_anonymous = self.request.user.is_anonymous

            # Check if the current user is not a member
            if is_anonymous or not team.members.filter(user=self.request.user).exists():
                if team.is_closed:
                    context['announcement_state'] = 'team closed'
                else:
                    context['announcement_state'] = 'team opened'
                    context['team'] = team
            # The current user is the team's member
            else:
                context['announcement_state'] = 'team member' 
        # The announcement has no team yet
        else:
            context['announcement_state'] = 'no team'
        
        return context


class AnnouncementList(ListView, AnnouncementStateContextMixin):
    template_name = 'webapp/announcement_list.html'
    context_object_name = 'announcements'
    paginate_by = 10 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar_active'] = 'announcement-list'
        context['filter_announcements'] = self.filter_announcements
        return context

    def get_queryset(self):
        qs = Announcement.objects.select_related('organization').order_by('created_on')
        # Filter announcements
        self.filter_announcements = AnnouncementFilter(self.request.GET, queryset=qs)
        voivodeship_id = self.request.GET.get('voivodeship')
        if voivodeship_id:
            filterd_qs = self.filter_announcements.qs.filter(organization__city__voivodeship_id=voivodeship_id)
        else:
            filterd_qs = self.filter_announcements.qs

        # Add announcement state info to the announcements
        for announcement in filterd_qs:
            announcement.extra_data = super().get_announcement_state(announcement)

        return filterd_qs


class AnnouncementDetails(DetailView, AnnouncementStateContextMixin):
    template_name = 'webapp/announcement_detail.html'
    context_object_name = 'announcement'

    def get_object(self):
        id = self.kwargs.get('id')
        return get_object_or_404(Announcement, id=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_author = context['announcement'].is_author(self.request.user)
        is_anonymous = self.request.user.is_anonymous

        context['is_author'] = is_author
        context['is_creator'] = False if is_anonymous else self.request.user.is_creator
        context.update(super().get_announcement_state(self.get_object()))
        if context['announcement_state'] == 'team opened':
            context['looking_for_form'] = TeamJoinForm(instance=context['team'])
        context['navbar_active'] = 'my-announcement' if is_author else None
        return context
            

class MyAnnouncement(TemplateView):
    template_name = 'webapp/announcement_empty.html'

    def get(self, request, *args, **kwargs):
        try:
            announcement = Announcement.objects.for_user(request.user)
        except Announcement.DoesNotExist:
            return super().get(request, *args, **kwargs)
        
        return redirect(reverse_lazy('webapp:announcement-detail', kwargs={'id': announcement.id}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar_active'] = 'my-announcement'
        return context


class AnnouncementCreate(UserIsOrganizationTestMixin, CreateView):
    template_name = 'webapp/announcement_edit.html'
    form_class = AnnouncementForm

    def form_valid(self, form):
        form.instance.organization = self.request.user.organization
        return super().form_valid(form)

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['organization'] = self.request.user.organization
        return context


class AnnouncementUpdate(UserIsOrganizationTestMixin, UpdateView):
    template_name = 'webapp/announcement_edit.html'
    form_class = AnnouncementForm

    def get_object(self):
        return Announcement.objects.for_user_or_400(self.request.user)

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['organization'] = self.request.user.organization
        return context


class AnnouncementDelete(UserIsOrganizationTestMixin, DeleteView):
    template_name = 'webapp/announcement_delete.html'
    success_url = reverse_lazy('webapp:index')
    
    def get_object(self):
        return Announcement.objects.for_user_or_400(self.request.user)


# ==== Teams ===== 
class MyTeams(UserIsCreatorTestMixin, ListView):
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
class EditProfile(LoginRequiredMixin, UpdateView):
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


# Forces all register views to activate "Zarejestruj się" navbar item
class RegisterContextMixin:
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