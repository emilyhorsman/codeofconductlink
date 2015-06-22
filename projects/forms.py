from django.forms import models
from profiles.recaptcha import ReCAPTCHAField
from .models import Project, Report

class CreateProjectForm(models.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'homepage', 'code_of_conduct', 'tags',)

    recaptcha = ReCAPTCHAField()
