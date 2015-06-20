from django import forms
from .models import ProjectSubmission

class NewProjectForm(forms.ModelForm):
    class Meta:
        model  = ProjectSubmission
        fields = ('name', 'homepage', 'tags')
