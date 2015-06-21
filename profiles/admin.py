from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(UserAdmin):
    # https://github.com/django/django/blob/master/django/contrib/auth/admin.py
    fieldsets = (
        (None, { 'fields': ('email', 'public_name', 'profile_slug', 'password') }),
    ) + UserAdmin.fieldsets[2:]

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    list_display = ('id', 'email', 'public_name', 'profile_slug')
    ordering = ('email',)
    search_fields = ('email', 'public_name', 'profile_slug')
