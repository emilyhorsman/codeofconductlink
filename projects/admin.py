from django.contrib import admin
from .models import Project, Submission, Report, Vouch

admin.site.register(Project)
admin.site.register(Submission)
admin.site.register(Report)
admin.site.register(Vouch)
