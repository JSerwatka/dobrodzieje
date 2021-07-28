from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
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