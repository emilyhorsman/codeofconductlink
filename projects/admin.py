from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Report, Project, ProjectSubmission, LinkSubmission, RepresentationSubmission

class ProjectSubmissionInline(admin.TabularInline):
    model = ProjectSubmission
    fields = ('user', 'name', 'homepage', 'tags')
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = (ProjectSubmissionInline,)
    list_display = ('id', 'user', 'created_date', '__str__')

@admin.register(ProjectSubmission)
class ProjectSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'project', 'name', 'homepage', 'tags', 'verified_date', 'created_date')

@admin.register(LinkSubmission)
class LinkSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'project', 'tag', 'url', 'project_has_tag', 'verified_date', 'created_date')

@admin.register(RepresentationSubmission)
class RepresentationSubmission(admin.ModelAdmin):
    list_display = ('id', 'user', 'project', 'tag', 'verified_date', 'created_date')

admin.site.register(Report)
