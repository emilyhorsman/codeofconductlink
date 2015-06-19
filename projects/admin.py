from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import SubmissionProfile

class SubmissionProfileInline(admin.StackedInline):
    model = SubmissionProfile

class CustomUserAdmin(UserAdmin):
    inlines = (SubmissionProfileInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
