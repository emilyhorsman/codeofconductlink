from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(UserAdmin):
    # https://github.com/django/django/blob/master/django/contrib/auth/admin.py
    fieldsets = (
        (None, { 'fields': ('email', 'profile_name', 'password') }),
    ) + UserAdmin.fieldsets[2:]

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    list_display = ('id', 'email', 'profile_name')
    ordering = ('email',)
    search_fields = ('email', 'profile_name')
