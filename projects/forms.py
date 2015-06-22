from profiles.recaptcha import ReCAPTCHAField
from common.forms import create_crispy_model_form

from .models import Project, Report
class CreateProjectForm(create_crispy_model_form(
                        legend_text='Submit a new project for tracking')):
    class Meta:
        model = Project
        fields = ('name', 'homepage', 'code_of_conduct', 'tags',)

    recaptcha = ReCAPTCHAField()

class UpdateProjectForm(create_crispy_model_form(
                        legend_text='Edit Project')):
    class Meta:
        model = Project
        fields = ('name', 'homepage', 'code_of_conduct', 'tags',)

class DeleteProjectForm(create_crispy_model_form(
                        legend_text='Are you sure you wish to delete this project?',
                        submit_text='Delete')):
    class Meta:
        model = Project
        fields = '__all__'
