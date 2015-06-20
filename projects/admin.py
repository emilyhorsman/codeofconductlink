from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Report, Project, LinkSubmission, RepresentationSubmission

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'homepage', 'tags', 'created_date', '__str__')

@admin.register(LinkSubmission)
class LinkSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'project', 'tag', 'url', 'project_has_tag', 'verified_date', 'created_date')

@admin.register(RepresentationSubmission)
class RepresentationSubmission(admin.ModelAdmin):
    list_display = ('id', 'user', 'project', 'tag', 'verified_date', 'created_date')

admin.site.register(Report)
