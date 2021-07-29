from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Organization, Creator, Announcement, Team, TeamMember


@admin.register(User)
class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email',)
    ordering = ('-date_joined',)
    list_filter = ('email', 'is_active', 'is_staff')
    list_display = ('email', 'is_active', 'is_staff')

    fieldsets = (
        (None, {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')})
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    search_fields = ('name', 'category')
    ordering = ('-name',)
    list_display = ('name', 'category', 'KRS')
    list_filter = ('category', )
    
    fieldsets = (
        ('Main', {'fields': ('user', 'name', 'KRS', 'category')}),
        ('Contact', {'fields': ('phone_number', 'fb_url', 'twitter_url')})
    )


@admin.register(Creator)
class CreatorAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name')
    ordering = ('-last_name',)
    list_display = ('user', 'first_name', 'last_name')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    search_fields = ('organization',)
    ordering = ('-organization',)
    list_display = ('organization', 'created_on')
    list_filter = ('organization', )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    ordering = ('-is_closed',)
    list_display = ('announcement', 'is_closed')
    list_filter = ('looking_for', 'our_stack')
    #TODO https://bradmontgomery.net/blog/django-admin-filters-arrayfields/


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('get_creator_str', 'get_team_str', 'role', 'is_admin')
    list_filter = ('role', 'is_admin')