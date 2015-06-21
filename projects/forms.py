from django.forms import models
from django.conf import settings
from authentication.recaptcha import ReCAPTCHAField
from .models import Project

class CreateProjectForm(models.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'homepage', 'tags',)

    recaptcha = ReCAPTCHAField()
