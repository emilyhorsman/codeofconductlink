from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import SubmissionProfile, Project, ProjectSubmission

admin.site.unregister(User)

class SubmissionProfileInline(admin.StackedInline):
    model = SubmissionProfile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (SubmissionProfileInline,)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_date', '__str__')

@admin.register(ProjectSubmission)
class ProjectSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'project', 'name', 'homepage', 'tags', 'is_verified', 'created_date')
