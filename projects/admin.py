from django.contrib import admin
import reversion
from .models import Project, Submission, Report, Vouch

class ProjectAdmin(reversion.VersionAdmin):
    pass

class SubmissionAdmin(reversion.VersionAdmin):
    pass

admin.site.register(Project, ProjectAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Report)
admin.site.register(Vouch)
